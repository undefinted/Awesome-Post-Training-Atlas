from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import yaml

from radar.main import (
    ATOM,
    ARXIV_API,
    ROOT,
    existing_ids,
    llm_triage,
    load_yaml,
    merge_source_record,
    normalize_arxiv_id,
    render_candidate_digest,
    urlopen_with_retry,
)


ARXIV_PATTERN = re.compile(r"(?i)(?:arxiv\.org/(?:abs|pdf)/|arxiv:)(\d{4}\.\d{4,5})(?:v\d+)?")


def github_readme(url: str) -> str:
    repo = url.rstrip("/").split("github.com/", 1)[1]
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/readme",
        headers={
            "Accept": "application/vnd.github.raw+json",
            "User-Agent": "Awesome-Post-Training-Atlas/0.2 (curated source backfill)",
        },
    )
    token = __import__("os").getenv("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urlopen_with_retry(request) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        return base64.b64decode(json.loads(payload)["content"]).decode("utf-8")
    return payload.decode("utf-8")


def source_inventory() -> dict[str, dict]:
    records: dict[str, dict] = {}
    sources = load_yaml(ROOT / "config" / "curated_sources.yaml")["sources"]
    for source in sources:
        readme = github_readme(source["url"])
        heading = ""
        for line in readme.splitlines():
            if line.lstrip().startswith("#"):
                heading = line.lstrip("# ").strip()
            context = f"{heading} {line}".lower()
            hints = infer_direction_hints(context)
            if not hints:
                hints = [source["primary_hint"]]
            for match in ARXIV_PATTERN.finditer(line):
                paper_id = f"arxiv:{match.group(1).lower()}"
                record = records.setdefault(paper_id, {"id": paper_id, "sources": [], "direction_hints": []})
                record["sources"] = sorted(set(record["sources"]) | {source["id"]})
                record["direction_hints"] = sorted(set(record["direction_hints"]) | set(hints))
    return records


def infer_direction_hints(text: str) -> list[str]:
    vocabulary = {
        "embodied-vla": ("embodied", "robot", "robotic", "vision-language-action", " vla", "autonomous driving"),
        "generative-media": ("diffusion", "image generation", "video generation", "text-to-image", "text-to-video", "dlm"),
        "multimodal": ("multimodal", "mllm", "vlm", "vision-language", "visual instruction", "visual reward"),
        "agentic": ("agent", "tool use", "web agent", "computer use", "coding agent", "multi-turn"),
        "distillation": ("distill", "teacher-student", "knowledge transfer"),
        "reward-verifiers": ("reward model", "verifier", "process reward", "outcome reward", "prm"),
        "preference-alignment": ("preference", "dpo", "rlhf", "rlaif", "alignment"),
        "reinforcement-learning": ("reinforcement", "rlvr", "grpo", "ppo", "policy optimization"),
        "supervised-adaptation": ("instruction tuning", "fine-tuning", "sft", "synthetic data", "data selection"),
        "reasoning-self-improvement": ("reasoning", "self-improvement", "self-training", "self-play", "self-correction"),
    }
    return [direction for direction, terms in vocabulary.items() if any(term in text for term in terms)]


def fetch_arxiv_ids(ids: list[str], batch_size: int = 40) -> dict[str, dict]:
    output = {}
    for offset in range(0, len(ids), batch_size):
        bare_ids = [paper_id.split(":", 1)[1] for paper_id in ids[offset : offset + batch_size]]
        params = urllib.parse.urlencode({"id_list": ",".join(bare_ids), "max_results": len(bare_ids)})
        request = urllib.request.Request(
            f"{ARXIV_API}?{params}",
            headers={"User-Agent": "Awesome-Post-Training-Atlas/0.2 (curated source backfill)"},
        )
        with urlopen_with_retry(request) as response:
            root = ET.fromstring(response.read())
        for entry in root.findall("atom:entry", ATOM):
            url = entry.findtext("atom:id", "", ATOM)
            paper_id = normalize_arxiv_id(url)
            output[paper_id] = {
                "id": paper_id,
                "title": " ".join(entry.findtext("atom:title", "", ATOM).split()),
                "date": entry.findtext("atom:published", "", ATOM)[:10],
                "updated": entry.findtext("atom:updated", "", ATOM)[:10],
                "url": f"https://arxiv.org/abs/{paper_id.split(':', 1)[1]}",
                "abstract": " ".join(entry.findtext("atom:summary", "", ATOM).split()),
                "authors": [node.findtext("atom:name", "", ATOM) for node in entry.findall("atom:author", ATOM)],
                "arxiv_categories": [node.attrib["term"] for node in entry.findall("atom:category", ATOM)],
            }
        if offset + batch_size < len(ids):
            time.sleep(3)
    return output


def render_report(records: dict[str, dict]) -> str:
    status_counts = Counter(record["status"] for record in records.values())
    source_counts = Counter(source for record in records.values() for source in record["sources"])
    direction_counts = Counter(direction for record in records.values() for direction in record["direction_hints"])
    lines = [
        "# Discovery coverage",
        "",
        f"Last indexed: **{dt.date.today().isoformat()}**.",
        "",
        "This report audits discoverability, not final inclusion. An item can be found in multiple curated sources and still require scope and metadata review.",
        "",
        f"- Unique arXiv IDs found: **{len(records)}**",
        f"- Already curated: **{status_counts['curated']}**",
        f"- Already queued or rejected: **{status_counts['decided']}**",
        f"- Newly discovered backlog: **{status_counts['unreviewed']}**",
        "",
        "## Source intersection",
        "",
        "| Source | Unique IDs referenced |",
        "|---|---:|",
    ]
    for source, count in source_counts.most_common():
        lines.append(f"| `{source}` | {count} |")
    lines.extend(["", "## Direction-hint coverage", "", "| Direction hint | Records |", "|---|---:|"])
    for direction, count in direction_counts.most_common():
        lines.append(f"| `{direction}` | {count} |")
    lines.extend(
        [
            "",
            "The weekly Backfill Radar prioritizes records supported by multiple sources, then balances review slots across direction hints. Exact inclusion remains governed by [TAXONOMY.md](TAXONOMY.md).",
            "",
        ]
    )
    return "\n".join(lines)


def update_candidates(records: dict[str, dict], maximum: int) -> int:
    unknown = [record for record in records.values() if record["status"] == "unreviewed"]
    unknown.sort(key=lambda record: (len(record["sources"]), record["id"]), reverse=True)
    # Preserve direction diversity before filling remaining slots by cross-source support.
    selected, seen = [], set()
    buckets = defaultdict(list)
    for record in unknown:
        for direction in record["direction_hints"]:
            buckets[direction].append(record)
    quota = max(1, maximum // max(1, len(buckets)))
    for direction in sorted(buckets):
        for record in buckets[direction][:quota]:
            if record["id"] not in seen:
                selected.append(record)
                seen.add(record["id"])
    for record in unknown:
        if len(selected) >= maximum:
            break
        if record["id"] not in seen:
            selected.append(record)
            seen.add(record["id"])
    metadata = fetch_arxiv_ids([record["id"] for record in selected[:maximum]])
    radar = load_yaml(ROOT / "config" / "radar.yaml")
    directions = load_yaml(ROOT / "config" / "taxonomy.yaml")["directions"]
    enriched = []
    for record in selected[:maximum]:
        paper = metadata.get(record["id"])
        if paper:
            paper["direction_hints"] = record["direction_hints"]
            enriched.append(paper)
    assessments = {}
    batch_size = radar["llm"]["batch_size"]
    for offset in range(0, len(enriched), batch_size):
        assessments.update(llm_triage(enriched[offset : offset + batch_size], radar["llm"], directions))
    path = ROOT / "data" / "candidates.yaml"
    existing = (load_yaml(path) or {}).get("papers", [])
    for paper in existing:
        curated_signals = [signal for signal in paper.get("source_signals", []) if signal.startswith("curated:")]
        if curated_signals:
            paper.setdefault("rule_score", 3 + 2 * (len(curated_signals) - 1))
            paper.setdefault("rule_reasons", [signal.replace("curated:", "curated-source:") for signal in curated_signals])
    merged = {paper["id"].lower(): paper for paper in existing}
    added = 0
    for record in selected[:maximum]:
        paper = metadata.get(record["id"])
        if not paper:
            continue
        paper["source_signals"] = [f"curated:{source}" for source in record["sources"]]
        paper["direction_hints"] = record["direction_hints"]
        paper["status"] = "candidate"
        paper["review_priority"] = len(record["sources"])
        paper["rule_score"] = 3 + 2 * (len(record["sources"]) - 1)
        paper["rule_reasons"] = [f"curated-source:{source}" for source in record["sources"]]
        paper["abstract"] = paper["abstract"][:1800].rstrip()
        assessment = assessments.get(paper["id"])
        if assessment:
            paper["llm_assessment"] = assessment
            if not assessment["include"] or assessment["relevance"] < radar["llm"]["minimum_relevance"]:
                continue
            paper["direction"] = assessment["direction"]
            paper["key_idea"] = assessment["key_idea"]
            paper["tags"] = assessment["tags"]
        if paper["id"] in merged:
            merge_source_record(merged[paper["id"]], paper)
        else:
            merged[paper["id"]] = paper
            added += 1
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        papers = list(merged.values())
        yaml.safe_dump({"papers": papers}, handle, sort_keys=False, allow_unicode=True, width=120)
    (ROOT / "data" / "CANDIDATES.md").write_text(render_candidate_digest(papers), encoding="utf-8", newline="\n")
    return added


def main() -> None:
    parser = argparse.ArgumentParser(description="Cross-check curated indexes and fill historical coverage gaps")
    parser.add_argument("--max-new", type=int, default=180)
    parser.add_argument("--inventory-only", action="store_true")
    args = parser.parse_args()
    records = source_inventory()
    curated = {paper["id"].lower() for paper in load_yaml(ROOT / "data" / "papers.yaml")["papers"]}
    decided = existing_ids() - curated
    for paper_id, record in records.items():
        record["status"] = "curated" if paper_id in curated else "decided" if paper_id in decided else "unreviewed"
    inventory_path = ROOT / "data" / "discovery_inventory.yaml"
    with inventory_path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump({"papers": sorted(records.values(), key=lambda record: record["id"])}, handle, sort_keys=False, allow_unicode=True, width=120)
    (ROOT / "DISCOVERY_COVERAGE.md").write_text(render_report(records), encoding="utf-8", newline="\n")
    added = 0 if args.inventory_only else update_candidates(records, args.max_new)
    print(f"Indexed {len(records)} unique IDs; added {added} candidates")


if __name__ == "__main__":
    main()
