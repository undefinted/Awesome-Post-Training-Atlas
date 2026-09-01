from __future__ import annotations

import argparse
import datetime as dt
from collections import Counter
from pathlib import Path

import yaml

from radar.main import (
    ROOT,
    balanced_shortlist,
    existing_ids,
    fetch_query_page,
    llm_triage,
    load_yaml,
    merge_source_record,
    render_candidate_digest,
    rule_score,
)


STATE_PATH = ROOT / "data" / "search_cursors.yaml"
AUDIT_PATH = ROOT / "data" / "search_audit.yaml"


def choose_direction(paper: dict) -> str:
    votes = Counter(key.rsplit(":", 1)[0] for key in paper.get("matched_queries", []))
    if votes:
        return sorted(votes, key=lambda direction: (-votes[direction], direction))[0]
    return (paper.get("direction_hints") or ["needs-review"])[0]


def load_state() -> dict:
    return load_yaml(STATE_PATH) if STATE_PATH.exists() else {"queries": {}}


def scan_academic_sources(since: str, until: str, pages_per_query: int) -> tuple[list[dict], dict]:
    radar = load_yaml(ROOT / "config" / "radar.yaml")
    state = load_state()
    found: dict[str, dict] = {}
    query_audit = []
    page_size = radar["arxiv"].get("page_size", 100)
    for index, spec in enumerate(radar["arxiv"]["queries"]):
        query = spec["query"] if isinstance(spec, dict) else spec
        direction = spec.get("direction", "unclassified") if isinstance(spec, dict) else "unclassified"
        key = f"{direction}:{index}"
        start = int(state["queries"].get(key, 0))
        scanned = in_window = 0
        reached_start = False
        for _ in range(pages_per_query):
            page = fetch_query_page(query, radar["arxiv"]["categories"], start, page_size)
            scanned += len(page)
            if not page:
                reached_start = True
                break
            for paper in page:
                if since <= paper["date"] <= until:
                    paper["direction_hints"] = [direction]
                    paper["source_signals"] = ["arxiv-backfill"]
                    paper["matched_queries"] = [key]
                    if paper["id"] in found:
                        merge_source_record(found[paper["id"]], paper)
                        found[paper["id"]]["matched_queries"] = sorted(
                            set(found[paper["id"]].get("matched_queries", [])) | {key}
                        )
                    else:
                        found[paper["id"]] = paper
                    in_window += 1
            start += len(page)
            if min(paper["date"] for paper in page) < since or len(page) < page_size:
                reached_start = True
                break
        state["queries"][key] = 0 if reached_start else start
        query_audit.append(
            {
                "key": key,
                "direction": direction,
                "query": query,
                "start_offset": int(state["queries"].get(key, 0)),
                "records_scanned": scanned,
                "records_in_window": in_window,
                "reached_since": reached_start,
            }
        )
    return list(found.values()), {"queries": query_audit, "state": state}


def prepare_candidates(papers: list[dict], maximum: int) -> list[dict]:
    radar = load_yaml(ROOT / "config" / "radar.yaml")
    known = existing_ids()
    eligible = []
    for paper in papers:
        if paper["id"] in known:
            continue
        score, reasons = rule_score(paper, radar["filter"])
        if score < radar["filter"]["minimum_score"]:
            continue
        paper["rule_score"] = score
        paper["rule_reasons"] = reasons
        paper["suggested_direction"] = choose_direction(paper)
        paper["classification_method"] = "academic-query-vote"
        eligible.append(paper)
    filter_config = dict(radar["filter"])
    filter_config["max_candidates_per_run"] = maximum
    shortlisted = balanced_shortlist(eligible, filter_config)
    directions = load_yaml(ROOT / "config" / "taxonomy.yaml")["directions"]
    assessments = {}
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


def write_outputs(candidates: list[dict], audit: dict, since: str, until: str) -> None:
    path = ROOT / "data" / "candidates.yaml"
    existing = (load_yaml(path) or {}).get("papers", [])
    for paper in existing:
        if not paper.get("llm_assessment"):
            paper["suggested_direction"] = choose_direction(paper)
            paper["classification_method"] = "academic-query-vote"
    merged = {paper["id"].lower(): paper for paper in existing}
    for paper in candidates:
        if paper["id"] in merged:
            merge_source_record(merged[paper["id"]], paper)
        else:
            merged[paper["id"]] = paper
    papers = list(merged.values())
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump({"papers": papers}, handle, sort_keys=False, allow_unicode=True, width=120)
    (ROOT / "data" / "CANDIDATES.md").write_text(render_candidate_digest(papers), encoding="utf-8", newline="\n")
    audit_payload = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "window": {"since": since, "until": until},
        "academic_sources": ["arxiv"],
        "queries": audit["queries"],
        "summary": {
            "records_scanned": sum(item["records_scanned"] for item in audit["queries"]),
            "records_in_window": sum(item["records_in_window"] for item in audit["queries"]),
            "unique_candidates_written": len(papers),
        },
    }
    with AUDIT_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(audit_payload, handle, sort_keys=False, allow_unicode=True, width=120)
    with STATE_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(audit["state"], handle, sort_keys=True, allow_unicode=True)
    counts = Counter(paper.get("direction") or paper.get("suggested_direction") or choose_direction(paper) for paper in papers)
    lines = [
        "# Academic discovery coverage",
        "",
        f"Last run: **{audit_payload['generated_at']}**.",
        f"Search window: **{since} through {until}**.",
        "",
        "Discovery is performed directly against academic indexes. Third-party GitHub lists are not ingestion sources and do not affect relevance or priority.",
        "",
        f"- arXiv records scanned this run: **{audit_payload['summary']['records_scanned']}**",
        f"- query matches inside the window: **{audit_payload['summary']['records_in_window']}**",
        f"- unresolved deduplicated candidates: **{len(papers)}**",
        "",
        "| Suggested direction | Candidates |",
        "|---|---:|",
    ]
    for direction, count in counts.most_common():
        lines.append(f"| `{direction}` | {count} |")
    lines.extend(["", "Exact queries, offsets, and per-query result counts are recorded in `data/search_audit.yaml`; pagination state is stored in `data/search_cursors.yaml`.", ""])
    (ROOT / "DISCOVERY_COVERAGE.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill directly from academic indexes")
    parser.add_argument("--since", default="2024-01-01")
    parser.add_argument("--until", default=dt.date.today().isoformat())
    parser.add_argument("--pages-per-query", type=int, default=1)
    parser.add_argument("--max-new", type=int, default=180)
    args = parser.parse_args()
    papers, audit = scan_academic_sources(args.since, args.until, args.pages_per_query)
    candidates = prepare_candidates(papers, args.max_new)
    write_outputs(candidates, audit, args.since, args.until)
    print(f"Scanned {sum(item['records_scanned'] for item in audit['queries'])} arXiv records; queued {len(candidates)} candidates")


if __name__ == "__main__":
    main()
