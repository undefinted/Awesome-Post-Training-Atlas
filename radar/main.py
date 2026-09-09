from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ARXIV_API = "https://export.arxiv.org/api/query"
HF_DAILY_API = "https://huggingface.co/api/daily_papers"
S2_API = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
CROSSREF_API = "https://api.crossref.org/works"
ATOM = {"atom": "http://www.w3.org/2005/Atom"}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def normalize_arxiv_id(url: str) -> str:
    value = url.rstrip("/").split("/")[-1]
    value = re.sub(r"v\d+$", "", value)
    return f"arxiv:{value.lower()}"


def normalize_doi(value: str) -> str:
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", str(value).strip(), flags=re.IGNORECASE)
    return f"doi:{value.lower()}"


def canonical_id(external_ids: dict | None = None, fallback: str | None = None) -> str:
    ids = external_ids or {}
    arxiv = ids.get("ArXiv") or ids.get("arxiv")
    if arxiv:
        return normalize_arxiv_id(str(arxiv))
    doi = ids.get("DOI") or ids.get("doi")
    if doi:
        return normalize_doi(str(doi))
    if fallback:
        return fallback.lower()
    raise ValueError("No stable academic identifier")


def strip_markup(value: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", value or "").split())


def date_from_parts(parts: list | None) -> str | None:
    if not parts:
        return None
    values = list(parts[0])
    if not values:
        return None
    values += [1] * (3 - len(values))
    try:
        return dt.date(int(values[0]), int(values[1]), int(values[2])).isoformat()
    except (TypeError, ValueError):
        return None


def extract_project_page(text: str) -> str | None:
    """Extract only URLs explicitly introduced as a project/homepage resource."""
    patterns = (
        r"(?:project\s+(?:page|homepage)|paper\s+homepage|homepage)\s*"
        r"(?:(?:is\s+)?(?:available\s+)?at|is|:)?\s*"
        r"(https?://[^\s<>\]\[{}\"']+)",
        r"(?:collection\s+of\s+related\s+papers|related\s+papers)\s+is\s+available\s+at\s+"
        r"(https?://[^\s<>\]\[{}\"']+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).rstrip(".,;:!?)")
    return None


def existing_ids() -> set[str]:
    ids: set[str] = set()
    for name in ("papers.yaml", "candidates.yaml", "rejected.yaml"):
        payload = load_yaml(ROOT / "data" / name) or {}
        ids.update(str(paper["id"]).lower() for paper in payload.get("papers", []))
    return ids


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def record_identity_keys(paper: dict) -> set[str]:
    keys = {str(paper["id"]).lower()}
    title = normalized_title(paper.get("title", ""))
    if title:
        keys.add(f"title:{title}")
    url = str(paper.get("url") or "")
    if "arxiv.org/" in url:
        keys.add(normalize_arxiv_id(url))
    if "doi.org/" in url:
        keys.add(normalize_doi(url))
    return keys


def existing_identity_keys() -> set[str]:
    keys: set[str] = set()
    for name in ("papers.yaml", "candidates.yaml", "rejected.yaml"):
        payload = load_yaml(ROOT / "data" / name) or {}
        for paper in payload.get("papers", []):
            keys.update(record_identity_keys(paper))
    return keys


def build_search(query: str, categories: list[str]) -> str:
    category_clause = " OR ".join(f"cat:{category}" for category in categories)
    return f"({query}) AND ({category_clause})"


def urlopen_with_retry(request: urllib.request.Request, timeout: int = 45, attempts: int = 3):
    error = None
    for attempt in range(attempts):
        try:
            return urllib.request.urlopen(request, timeout=timeout)
        except Exception as exc:  # network services occasionally throttle or return 5xx
            error = exc
            if attempt + 1 < attempts:
                retry_after = 0
                if isinstance(exc, HTTPError) and exc.code == 429:
                    try:
                        retry_after = int(exc.headers.get("Retry-After", "0"))
                    except (TypeError, ValueError):
                        retry_after = 0
                # arXiv commonly needs a materially longer pause than a generic 5xx.
                delay = retry_after or ((10 * (attempt + 1)) if isinstance(exc, HTTPError) and exc.code == 429 else 2 ** attempt)
                time.sleep(min(delay, 45))
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
        paper = {
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
        project_page = extract_project_page(abstract)
        if project_page:
            paper["project_page"] = project_page
        papers.append(paper)
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


def fetch_semantic_scholar(query: str, direction: str, start_date: str, end_date: str, limit: int) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "query": query,
            "publicationDateOrYear": f"{start_date}:{end_date}",
            "fields": "title,abstract,authors,publicationDate,url,externalIds,openAccessPdf,venue",
            "limit": limit,
        }
    )
    headers = {"User-Agent": "Awesome-Post-Training-Atlas/0.1 (GitHub paper radar)"}
    if os.getenv("SEMANTIC_SCHOLAR_API_KEY"):
        headers["x-api-key"] = os.environ["SEMANTIC_SCHOLAR_API_KEY"]
    request = urllib.request.Request(f"{S2_API}?{params}", headers=headers)
    with urlopen_with_retry(request) as response:
        payload = json.loads(response.read())
    papers = []
    for item in payload.get("data", [])[:limit]:
        external = item.get("externalIds") or {}
        paper_id = canonical_id(external, f"semantic-scholar:{item['paperId']}")
        arxiv = external.get("ArXiv")
        doi = external.get("DOI")
        open_pdf = (item.get("openAccessPdf") or {}).get("url")
        primary_url = (
            f"https://arxiv.org/abs/{arxiv}" if arxiv else f"https://doi.org/{doi}" if doi else item.get("url")
        )
        date = item.get("publicationDate")
        if not date or not primary_url or not item.get("authors"):
            continue
        papers.append(
            {
                "id": paper_id,
                "title": item.get("title") or paper_id,
                "date": date,
                "updated": date,
                "url": primary_url,
                "abstract": item.get("abstract") or "",
                "authors": [a.get("name", "") for a in item.get("authors", []) if a.get("name")],
                "source_signals": ["semantic-scholar"],
                "source_links": {"semantic_scholar": item.get("url")},
                "direction_hints": [direction],
                **({"open_access_pdf": open_pdf} if open_pdf else {}),
                **({"venue": item.get("venue"), "venue_source": item.get("url")} if item.get("venue") else {}),
            }
        )
    return papers


def fetch_crossref(query: str, direction: str, start_date: str, end_date: str, rows: int) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "query.bibliographic": query,
            "filter": f"from-created-date:{start_date},until-created-date:{end_date}",
            "rows": rows,
            "select": "DOI,title,author,abstract,created,URL,published,container-title,type",
        }
    )
    request = urllib.request.Request(
        f"{CROSSREF_API}?{params}",
        headers={"User-Agent": "Awesome-Post-Training-Atlas/0.1 (GitHub paper radar)"},
    )
    with urlopen_with_retry(request) as response:
        payload = json.loads(response.read())
    papers = []
    for item in payload.get("message", {}).get("items", []):
        doi = item.get("DOI")
        created = str((item.get("created") or {}).get("date-time") or "")[:10]
        published_parts = (item.get("published") or {}).get("date-parts")
        published = date_from_parts(published_parts)
        if published_parts and len(published_parts[0]) < 3:
            published = None
        # The deposit date is the observable public discovery date. Some
        # publishers deposit records carrying a future or year-only date.
        date = published if published and published <= end_date else created
        titles = item.get("title") or []
        if not doi or not date or not titles or not item.get("author"):
            continue
        authors = []
        for author in item.get("author", []):
            name = " ".join(part for part in (author.get("given"), author.get("family")) if part)
            if name:
                authors.append(name)
        venue = (item.get("container-title") or [None])[0]
        url = f"https://doi.org/{doi}"
        papers.append(
            {
                "id": normalize_doi(doi),
                "title": strip_markup(titles[0]),
                "date": date,
                "updated": created or date,
                "url": url,
                "abstract": strip_markup(item.get("abstract") or ""),
                "authors": authors,
                "source_signals": ["crossref"],
                "source_links": {"crossref": item.get("URL") or url},
                "direction_hints": [direction],
                **({"venue": strip_markup(venue), "venue_source": url} if venue else {}),
            }
        )
    return papers


def merge_source_record(target: dict, incoming: dict) -> None:
    target["source_signals"] = sorted(set(target.get("source_signals", [])) | set(incoming.get("source_signals", [])))
    for key in ("huggingface", "code", "project_page"):
        if incoming.get(key):
            target[key] = incoming[key]
    target["source_links"] = {**target.get("source_links", {}), **incoming.get("source_links", {})}
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


def academic_index_relevant(paper: dict, config: dict) -> bool:
    """Reject generic domain RL while keeping cross-modality post-training."""
    signals = set(paper.get("source_signals", []))
    if not signals & {"semantic-scholar", "crossref"}:
        return True
    text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
    method_terms = [term.lower() for term in config.get("required_method_terms", [])]
    scope_terms = [term.lower() for term in config.get("required_scope_terms", [])]
    has_method = any(term in text for term in method_terms)
    has_scope = any(term in text for term in scope_terms)
    return has_method and has_scope


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
    known = existing_identity_keys()
    cutoff = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    submitted_from = cutoff.replace("-", "") + "0000"
    submitted_to = dt.date.today().isoformat().replace("-", "") + "2359"
    found: dict[str, dict] = {}
    found_keys: dict[str, str] = {}

    def store_found(paper: dict) -> None:
        keys = record_identity_keys(paper)
        if keys & known:
            return
        matched_id = next((found_keys[key] for key in keys if key in found_keys), None)
        if matched_id:
            merge_source_record(found[matched_id], paper)
            for key in keys:
                found_keys[key] = matched_id
            return
        found[paper["id"]] = paper
        for key in keys:
            found_keys[key] = paper["id"]
    for index, spec in enumerate(radar["arxiv"]["queries"]):
        if index:
            time.sleep(3)
        query = spec["query"] if isinstance(spec, dict) else spec
        dated_query = f"({query}) AND submittedDate:[{submitted_from} TO {submitted_to}]"
        direction = spec.get("direction") if isinstance(spec, dict) else None
        try:
            query_papers = fetch_query(
                dated_query,
                radar["arxiv"]["categories"],
                radar["arxiv"]["max_results_per_query"],
                radar["arxiv"].get("page_size", 100),
            )
        except Exception as exc:
            # Preserve useful results from other independent queries. A transient
            # failure must not discard the entire daily discovery run.
            print(f"Warning: skipping failed arXiv query {query!r}: {exc}", file=sys.stderr)
            if isinstance(exc, HTTPError) and exc.code == 429:
                print("Warning: arXiv is throttling this runner; continuing with other academic signals.", file=sys.stderr)
                break
            continue
        for paper in query_papers:
            if direction:
                paper["direction_hints"] = [direction]
            if paper["date"] >= cutoff:
                store_found(paper)
    if radar.get("huggingface_daily", {}).get("enabled"):
        try:
            daily_papers = fetch_huggingface_daily(days, radar["huggingface_daily"]["limit"])
        except Exception as exc:
            # Hugging Face is an auxiliary discovery signal. Its API changing or
            # being unavailable must not discard papers already found on arXiv.
            print(f"Warning: skipping unavailable Hugging Face daily signal: {exc}", file=sys.stderr)
            daily_papers = []
        for paper in daily_papers:
            store_found(paper)
    indexes = radar.get("academic_indexes", {})
    index_cutoff = (
        dt.date.today() - dt.timedelta(days=max(days, int(indexes.get("lookback_days", days))))
    ).isoformat()
    for spec in indexes.get("queries", []):
        sources = []
        if indexes.get("semantic_scholar", {}).get("enabled"):
            sources.append(
                (
                    "Semantic Scholar",
                    fetch_semantic_scholar,
                    (spec["query"], spec["direction"], index_cutoff, dt.date.today().isoformat(), indexes["semantic_scholar"]["limit_per_query"]),
                )
            )
        if indexes.get("crossref", {}).get("enabled"):
            sources.append(
                (
                    "Crossref",
                    fetch_crossref,
                    (spec["query"], spec["direction"], index_cutoff, dt.date.today().isoformat(), indexes["crossref"]["rows_per_query"]),
                )
            )
        for source_name, fetcher, arguments in sources:
            try:
                indexed_papers = fetcher(*arguments)
            except Exception as exc:
                print(f"Warning: skipping unavailable {source_name} query {spec['query']!r}: {exc}", file=sys.stderr)
                continue
            for paper in indexed_papers:
                store_found(paper)
    shortlisted = []
    for paper in found.values():
        if not academic_index_relevant(paper, indexes):
            continue
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
        elif paper.get("direction_hints"):
            # Scheduled runs intentionally work without an LLM key. In that
            # mode the query's reviewed taxonomy mapping is the deterministic
            # fallback, so every candidate remains renderable and auditable.
            paper["direction"] = paper["direction_hints"][0]
        else:
            # An auxiliary-only record has no defensible taxonomy assignment.
            continue
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
    checked_at = dt.datetime.now(dt.timezone.utc).astimezone(dt.timezone(dt.timedelta(hours=8))).replace(microsecond=0)
    with (ROOT / "data" / "radar_status.yaml").open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(
            {"last_successful_discovery_at": checked_at.isoformat(), "timezone": "Asia/Shanghai"},
            handle,
            sort_keys=False,
            allow_unicode=True,
        )
    print(f"Candidates: {len(papers)}")


if __name__ == "__main__":
    main()
