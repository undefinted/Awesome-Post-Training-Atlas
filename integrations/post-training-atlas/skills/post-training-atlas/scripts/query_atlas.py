#!/usr/bin/env python3
"""Query the Awesome-Post-Training-Atlas YAML data from any compatible harness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised by the user environment
    raise SystemExit("PyYAML is required. Install the atlas repository requirements first.") from exc


def load_records(root: Path) -> list[dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for filename in ("data/papers.yaml", "data/candidates.yaml"):
        path = root / filename
        if not path.exists():
            continue
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for paper in payload.get("papers", []):
            key = str(paper.get("id", "")).lower()
            if not key:
                continue
            if key not in records:
                records[key] = dict(paper)
                continue
            current = records[key]
            for field in ("direction_hints", "source_signals", "matched_queries", "auto_labels"):
                values = sorted(set(current.get(field, [])) | set(paper.get(field, [])))
                if values:
                    current[field] = values
            for field in ("code", "huggingface", "venue", "venue_type", "venue_url", "institutions"):
                if paper.get(field) and not current.get(field):
                    current[field] = paper[field]
    return list(records.values())


def matches(paper: dict[str, Any], args: argparse.Namespace) -> bool:
    haystack = " ".join(
        str(value)
        for value in (
            paper.get("title", ""),
            paper.get("abstract", ""),
            paper.get("key_idea", ""),
            " ".join(paper.get("tags", [])),
            " ".join(paper.get("auto_labels", [])),
        )
    ).lower()
    if args.query and args.query.lower() not in haystack:
        return False
    direction_ids = set(paper.get("direction_hints", []))
    direction_ids.add(paper.get("direction") or paper.get("suggested_direction"))
    if args.direction and args.direction not in direction_ids:
        return False
    date = str(paper.get("date", ""))
    if args.year and not date.startswith(str(args.year)):
        return False
    if args.month and date[:7] != args.month:
        return False
    labels = set(paper.get("auto_labels", [])) | set(paper.get("tags", []))
    if args.label and not set(args.label).issubset(labels):
        return False
    if args.status:
        discovery = bool(paper.get("discovery_candidate")) or paper.get("status") == "candidate"
        status = "discovery" if discovery else "curated"
        if status != args.status:
            return False
    return True


def compact(paper: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "id",
        "title",
        "date",
        "direction",
        "url",
        "key_idea",
        "tags",
        "auto_labels",
        "authors",
        "institutions",
        "venue",
        "venue_type",
        "discovery_candidate",
    )
    result = {key: paper[key] for key in keys if paper.get(key) not in (None, [], "")}
    if "direction" not in result:
        result["direction"] = paper.get("suggested_direction") or (paper.get("direction_hints") or [None])[0]
    result["status"] = "discovery" if paper.get("discovery_candidate") or paper.get("status") == "candidate" else "curated"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Atlas repository root")
    parser.add_argument("--query", help="Search title, abstract, key idea, tags, and labels")
    parser.add_argument("--direction", help="Primary direction ID, e.g. agentic")
    parser.add_argument("--year", type=int)
    parser.add_argument("--month", help="YYYY-MM")
    parser.add_argument("--label", action="append", help="Require a label; repeat for ALL semantics")
    parser.add_argument("--status", choices=("curated", "discovery"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    results = [paper for paper in load_records(args.root) if matches(paper, args)]
    results.sort(key=lambda paper: (str(paper.get("date", "")), str(paper.get("title", ""))), reverse=True)
    results = [compact(paper) for paper in results[: max(args.limit, 0)]]
    if args.as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    for paper in results:
        labels = ", ".join(paper.get("auto_labels", []) or paper.get("tags", []))
        print(f"- {paper.get('title', 'Untitled')} ({paper.get('date', '?')}) [{paper.get('direction', '?')}]" + (f" · {labels}" if labels else ""))
        print(f"  {paper.get('url', '')}")
    print(f"\nMatched {len(results)} record(s). Use --json for structured output.")


if __name__ == "__main__":
    main()
