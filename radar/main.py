from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ARXIV_API = "https://export.arxiv.org/api/query"
HF_DAILY_API = "https://huggingface.co/api/daily_papers"
ATOM = {"atom": "http://www.w3.org/2005/Atom"}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def normalize_arxiv_id(url: str) -> str:
    value = url.rstrip("/").split("/")[-1]
    value = re.sub(r"v\d+$", "", value)
    return f"arxiv:{value.lower()}"


def existing_ids() -> set[str]:
    ids: set[str] = set()
    for name in ("papers.yaml", "candidates.yaml", "rejected.yaml"):
        payload = load_yaml(ROOT / "data" / name) or {}
        ids.update(str(paper["id"]).lower() for paper in payload.get("papers", []))
    return ids


def build_search(query: str, categories: list[str]) -> str:
    category_clause = " OR ".join(f"cat:{category}" for category in categories)
    return f"({query}) AND ({category_clause})"


def urlopen_with_retry(request: urllib.request.Request, timeout: int = 45, attempts: int = 4):
    error = None
    for attempt in range(attempts):
        try:
            return urllib.request.urlopen(request, timeout=timeout)
        except Exception as exc:  # network services occasionally throttle or return 5xx
            error = exc
            if attempt + 1 < attempts:
                time.sleep(2 ** attempt)
    raise error


def fetch_query_page(query: str, categories: list[str], start: int, maximum: int) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "search_query": build_search(query, categories),
            "start": start,
            "max_results": maximum,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    request = urllib.request.Request(
        f"{ARXIV_API}?{params}",
        headers={"User-Agent": "Awesome-Post-Training-Atlas/0.1 (GitHub paper radar)"},
    )
    with urlopen_with_retry(request) as response:
        root = ET.fromstring(response.read())
    papers = []
    for entry in root.findall("atom:entry", ATOM):
        abstract = " ".join((entry.findtext("atom:summary", "", ATOM)).split())
        title = " ".join((entry.findtext("atom:title", "", ATOM)).split())
        url = entry.findtext("atom:id", "", ATOM)
        paper_id = normalize_arxiv_id(url)
        categories_found = [node.attrib["term"] for node in entry.findall("atom:category", ATOM)]
        papers.append(
            {
                "id": paper_id,
                "title": title,
                "date": entry.findtext("atom:published", "", ATOM)[:10],
                "updated": entry.findtext("atom:updated", "", ATOM)[:10],
                "url": f"https://arxiv.org/abs/{paper_id.split(':', 1)[1]}",
                "abstract": abstract,
                "authors": [node.findtext("atom:name", "", ATOM) for node in entry.findall("atom:author", ATOM)],
                "arxiv_categories": categories_found,
                "source_signals": ["arxiv"],
            }
        )
    return papers


def fetch_query(query: str, categories: list[str], maximum: int, page_size: int = 100) -> list[dict]:
    papers = []
    for start in range(0, maximum, page_size):
        page = fetch_query_page(query, categories, start, min(page_size, maximum - start))
        papers.extend(page)
        if len(page) < min(page_size, maximum - start):
            break
        time.sleep(3)
    return papers


def fetch_huggingface_daily(days: int, limit: int) -> list[dict]:
    cutoff = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    request = urllib.request.Request(
        f"{HF_DAILY_API}?{urllib.parse.urlencode({'limit': limit})}",
        headers={"User-Agent": "Awesome-Post-Training-Atlas/0.1 (GitHub paper radar)"},
    )
    with urlopen_with_retry(request) as response:
        payload = json.loads(response.read())
    papers = []
    for item in payload:
        paper = item.get("paper") or {}
        arxiv_id = str(paper.get("id") or "").strip()
        submitted = str(paper.get("submittedOnDailyAt") or item.get("publishedAt") or "")[:10]
        if not arxiv_id or submitted < cutoff:
            continue
        published = str(paper.get("publishedAt") or item.get("publishedAt") or submitted)[:10]
        authors = [author.get("name", "") for author in paper.get("authors", []) if author.get("name")]
        candidate = {
            "id": f"arxiv:{arxiv_id.lower()}",
            "title": paper.get("title") or item.get("title") or arxiv_id,
            "date": published,
            "updated": submitted,
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "abstract": paper.get("summary") or item.get("summary") or "",
            "authors": authors,
            "arxiv_categories": [],
            "source_signals": ["huggingface-daily"],
            "huggingface": {
                "url": f"https://huggingface.co/papers/{arxiv_id}",
                "upvotes": int(paper.get("upvotes") or 0),
            },
        }
        if paper.get("githubRepo"):
            candidate["code"] = paper["githubRepo"]
        papers.append(candidate)
    return papers


def merge_source_record(target: dict, incoming: dict) -> None:
    target["source_signals"] = sorted(set(target.get("source_signals", [])) | set(incoming.get("source_signals", [])))
    for key in ("huggingface", "code"):
        if incoming.get(key):
            target[key] = incoming[key]
    target["direction_hints"] = sorted(
        set(target.get("direction_hints", [])) | set(incoming.get("direction_hints", []))
    )


def balanced_shortlist(papers: list[dict], config: dict) -> list[dict]:
    """Keep one broad query or hot topic from starving smaller directions."""
    ordered = sorted(papers, key=lambda paper: (paper["date"], paper["rule_score"]), reverse=True)
    per_direction = int(config["max_candidates_per_direction"])
    total = int(config["max_candidates_per_run"])
    selected = []
    selected_ids = set()
    counts = defaultdict(int)
    for paper in ordered:
        hints = paper.get("direction_hints") or ["unclassified"]
        available = [hint for hint in hints if counts[hint] < per_direction]
        if not available:
            continue
        bucket = min(available, key=lambda hint: counts[hint])
        counts[bucket] += 1
        selected.append(paper)
        selected_ids.add(paper["id"])
        if len(selected) == total:
            return selected
    for paper in ordered:
        if paper["id"] not in selected_ids:
            selected.append(paper)
            if len(selected) == total:
                break
    return selected


def rule_score(paper: dict, config: dict) -> tuple[int, list[str]]:
    text = f"{paper['title']} {paper['abstract']}".lower()
    score = 0
    reasons = []
    for term, weight in config["positive_terms"].items():
        if term.lower() in text:
            score += int(weight)
            reasons.append(f"+{weight}:{term}")
    for term, weight in config["negative_terms"].items():
        if term.lower() in text:
            score += int(weight)
            reasons.append(f"{weight}:{term}")
    return score, reasons


def extract_response_text(payload: dict) -> str:
    for item in payload.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return content["text"]
    raise RuntimeError("OpenAI response did not contain output_text")


def llm_triage(papers: list[dict], config: dict, directions: list[dict]) -> dict[str, dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not papers:
        return {}
    model = os.getenv("OPENAI_MODEL") or config["default_model"]
    direction_ids = [item["id"] for item in directions]
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["assessments"],
        "properties": {
            "assessments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "include", "relevance", "direction", "key_idea", "rationale", "tags"],
                    "properties": {
                        "id": {"type": "string"},
                        "include": {"type": "boolean"},
                        "relevance": {"type": "number", "minimum": 0, "maximum": 1},
                        "direction": {"type": "string", "enum": direction_ids},
                        "key_idea": {"type": "string"},
                        "rationale": {"type": "string"},
                        "tags": {"type": "array", "items": {"type": "string"}, "maxItems": 8},
                    },
                },
            }
        },
    }
    compact = [
        {"id": p["id"], "title": p["title"], "abstract": p["abstract"][:4000]}
        for p in papers
    ]
    prompt = (
        "Assess candidate papers for a cross-modality post-training research atlas. "
        "Include only work that changes a pretrained foundation model through supervised adaptation, "
        "preferences, rewards, verifiers, RL, self-improvement, tool/environment interaction, or equivalent "
        "multimodal/embodied feedback. Exclude inference-only methods, ordinary applications, and post-training "
        "quantization. Be conservative. key_idea must be one factual sentence.\n\n"
        f"Directions: {json.dumps(directions, ensure_ascii=False)}\n\n"
        f"Papers: {json.dumps(compact, ensure_ascii=False)}"
    )
    body = json.dumps(
        {
            "model": model,
            "store": False,
            "input": prompt,
            "text": {"format": {"type": "json_schema", "name": "paper_triage", "strict": True, "schema": schema}},
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=body,
        method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read())
    parsed = json.loads(extract_response_text(result))
    return {item["id"].lower(): item for item in parsed["assessments"]}


def discover(days: int) -> list[dict]:
    radar = load_yaml(ROOT / "config" / "radar.yaml")
    directions = load_yaml(ROOT / "config" / "taxonomy.yaml")["directions"]
    known = existing_ids()
    cutoff = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    found: dict[str, dict] = {}
    for index, spec in enumerate(radar["arxiv"]["queries"]):
        if index:
            time.sleep(3)
        query = spec["query"] if isinstance(spec, dict) else spec
        direction = spec.get("direction") if isinstance(spec, dict) else None
        for paper in fetch_query(
            query,
            radar["arxiv"]["categories"],
            radar["arxiv"]["max_results_per_query"],
            radar["arxiv"].get("page_size", 100),
        ):
            if direction:
                paper["direction_hints"] = [direction]
            if paper["date"] >= cutoff and paper["id"] not in known:
                if paper["id"] in found:
                    merge_source_record(found[paper["id"]], paper)
                else:
                    found[paper["id"]] = paper
    if radar.get("huggingface_daily", {}).get("enabled"):
        for paper in fetch_huggingface_daily(days, radar["huggingface_daily"]["limit"]):
            if paper["id"] in known:
                continue
            if paper["id"] in found:
                merge_source_record(found[paper["id"]], paper)
            else:
                found[paper["id"]] = paper
    shortlisted = []
    for paper in found.values():
        score, reasons = rule_score(paper, radar["filter"])
        if score >= radar["filter"]["minimum_score"]:
            paper["rule_score"] = score
            paper["rule_reasons"] = reasons
            shortlisted.append(paper)
    shortlisted = balanced_shortlist(shortlisted, radar["filter"])
    assessments: dict[str, dict] = {}
    size = radar["llm"]["batch_size"]
    for offset in range(0, len(shortlisted), size):
        assessments.update(llm_triage(shortlisted[offset : offset + size], radar["llm"], directions))
    output = []
    for paper in shortlisted:
        assessment = assessments.get(paper["id"])
        if assessment:
            paper["llm_assessment"] = assessment
            if not assessment["include"] or assessment["relevance"] < radar["llm"]["minimum_relevance"]:
                continue
            paper["direction"] = assessment["direction"]
            paper["key_idea"] = assessment["key_idea"]
            paper["tags"] = assessment["tags"]
        paper["abstract"] = paper["abstract"][: radar["filter"]["stored_abstract_characters"]].rstrip()
        paper["status"] = "candidate"
        output.append(paper)
    return output


def render_candidate_digest(papers: list[dict]) -> str:
    lines = [
        "# Radar candidates",
        "",
        "Automated proposals only; inclusion requires human review.",
        "",
        "| Date | Paper | Sources | Signal | Suggested direction |",
        "|---|---|---|---:|---|",
    ]
    for paper in papers:
        title = paper["title"].replace("|", "\\|")
        direction = paper.get("direction", "needs-review")
        sources = ", ".join(paper.get("source_signals", []))
        hf = paper.get("huggingface", {})
        signal = str(paper.get("rule_score", paper.get("review_priority", "-")))
        if hf:
            signal += f" / HF ↑{hf.get('upvotes', 0)}"
        lines.append(f"| {paper['date']} | [{title}]({paper['url']}) | {sources} | {signal} | `{direction}` |")
    lines.extend(
        [
            "",
            "Review checklist:",
            "",
            "- Is there an actual learning or feedback loop after pretraining?",
            "- Is the primary direction correct?",
            "- Is the key idea factual and specific?",
            "- Is this already represented by another version or publication?",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover recent post-training papers")
    parser.add_argument("--days", type=int, default=8)
    args = parser.parse_args()
    path = ROOT / "data" / "candidates.yaml"
    existing = (load_yaml(path) or {}).get("papers", [])
    merged = {paper["id"].lower(): paper for paper in existing}
    for paper in discover(args.days):
        merged[paper["id"].lower()] = paper
    papers = list(merged.values())
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump({"papers": papers}, handle, sort_keys=False, allow_unicode=True, width=120)
    (ROOT / "data" / "CANDIDATES.md").write_text(render_candidate_digest(papers), encoding="utf-8", newline="\n")
    print(f"Candidates: {len(papers)}")


if __name__ == "__main__":
    main()
