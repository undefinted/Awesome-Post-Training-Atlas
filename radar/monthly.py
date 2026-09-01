from __future__ import annotations

import argparse
import calendar
import datetime as dt
import time
from collections import defaultdict
from pathlib import Path

import yaml

from radar.main import ROOT, existing_ids, fetch_query, load_yaml, merge_source_record, render_candidate_digest, rule_score
from radar.render import update_readme


AUDIT_PATH = ROOT / "data" / "monthly_audit.yaml"


def month_bounds(year: int, month: int) -> tuple[str, str, str, str]:
    last = calendar.monthrange(year, month)[1]
    start_date = f"{year:04d}-{month:02d}-01"
    end_date = f"{year:04d}-{month:02d}-{last:02d}"
    return start_date, end_date, f"{year:04d}{month:02d}010000", f"{year:04d}{month:02d}{last:02d}2359"


def grouped_queries() -> dict[str, list[str]]:
    radar = load_yaml(ROOT / "config" / "radar.yaml")
    grouped = defaultdict(list)
    for spec in radar["arxiv"]["queries"]:
        grouped[spec["direction"]].append(spec["query"])
    return grouped


def scan_cell(direction: str, queries: list[str], year: int, month: int, maximum: int) -> tuple[list[dict], dict]:
    radar = load_yaml(ROOT / "config" / "radar.yaml")
    start_date, end_date, start_stamp, end_stamp = month_bounds(year, month)
    combined = " OR ".join(f"({query})" for query in queries)
    dated_query = f"({combined}) AND submittedDate:[{start_stamp} TO {end_stamp}]"
    papers = fetch_query(
        dated_query,
        radar["arxiv"]["categories"],
        maximum,
        radar["arxiv"].get("page_size", 100),
    )
    eligible = []
    for paper in papers:
        if not (start_date <= paper["date"] <= end_date):
            continue
        score, reasons = rule_score(paper, radar["filter"])
        if score < radar["filter"]["minimum_score"]:
            continue
        paper["rule_score"] = score
        paper["rule_reasons"] = reasons
        paper["direction_hints"] = [direction]
        paper["suggested_direction"] = direction
        paper["classification_method"] = "direction-month-query"
        paper["source_signals"] = ["arxiv-monthly-backfill"]
        paper["matched_queries"] = [f"{direction}:{year:04d}-{month:02d}"]
        paper["status"] = "candidate"
        paper["abstract"] = paper["abstract"][: radar["filter"]["stored_abstract_characters"]].rstrip()
        eligible.append(paper)
    eligible.sort(key=lambda paper: (paper["rule_score"], paper["date"]), reverse=True)
    return eligible, {
        "cell": f"{direction}:{year:04d}-{month:02d}",
        "direction": direction,
        "month": f"{year:04d}-{month:02d}",
        "query": dated_query,
        "records_scanned": len(papers),
        "eligible": len(eligible),
        "complete": len(papers) < maximum,
    }


def run(years: list[int], months: list[int], max_per_cell: int) -> None:
    grouped = grouped_queries()
    known = existing_ids()
    candidate_path = ROOT / "data" / "candidates.yaml"
    existing = (load_yaml(candidate_path) or {}).get("papers", [])
    merged = {paper["id"].lower(): paper for paper in existing}
    audit = (load_yaml(AUDIT_PATH) or {"cells": []}) if AUDIT_PATH.exists() else {"cells": []}
    audit_by_cell = {cell["cell"]: cell for cell in audit.get("cells", [])}
    added = 0

    def checkpoint() -> None:
        papers = list(merged.values())
        with candidate_path.open("w", encoding="utf-8", newline="\n") as handle:
            yaml.safe_dump({"papers": papers}, handle, sort_keys=False, allow_unicode=True, width=120)
        (ROOT / "data" / "CANDIDATES.md").write_text(render_candidate_digest(papers), encoding="utf-8", newline="\n")
        with AUDIT_PATH.open("w", encoding="utf-8", newline="\n") as handle:
            yaml.safe_dump({"cells": sorted(audit_by_cell.values(), key=lambda cell: cell["cell"])}, handle, sort_keys=False, allow_unicode=True, width=160)
        update_readme()

    for year in years:
        for month in months:
            if dt.date(year, month, 1) > dt.date.today().replace(day=1):
                continue
            for direction, queries in grouped.items():
                cell_id = f"{direction}:{year:04d}-{month:02d}"
                try:
                    papers, cell = scan_cell(direction, queries, year, month, max_per_cell)
                except Exception as exc:
                    audit_by_cell[cell_id] = {
                        "cell": cell_id,
                        "direction": direction,
                        "month": f"{year:04d}-{month:02d}",
                        "complete": False,
                        "error": f"{type(exc).__name__}: {exc}",
                        "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                    }
                    safe_error = str(exc).encode("ascii", "backslashreplace").decode("ascii")
                    print(f"{cell_id}: ERROR {type(exc).__name__}: {safe_error}")
                    time.sleep(2)
                    continue
                queued = 0
                for paper in papers:
                    if paper["id"] in known:
                        continue
                    if paper["id"] in merged:
                        merge_source_record(merged[paper["id"]], paper)
                    else:
                        merged[paper["id"]] = paper
                        known.add(paper["id"])
                        added += 1
                        queued += 1
                cell["newly_queued"] = queued
                cell["checked_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
                audit_by_cell[cell["cell"]] = cell
                print(f"{cell['cell']}: scanned={cell['records_scanned']} eligible={cell['eligible']} new={queued}")
                time.sleep(1)
            checkpoint()
    checkpoint()
    print(f"Added {added} unique candidates; total unresolved candidates={len(merged)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit and backfill every direction-month cell directly from arXiv")
    parser.add_argument("--year", type=int, action="append")
    parser.add_argument("--month", type=int, action="append", choices=range(1, 13))
    parser.add_argument("--auto", action="store_true", help="scan the newest direction-month grid not yet fully audited")
    parser.add_argument("--max-per-cell", type=int, default=300)
    args = parser.parse_args()
    if args.auto:
        audit = (load_yaml(AUDIT_PATH) or {"cells": []}) if AUDIT_PATH.exists() else {"cells": []}
        covered = {
            (cell["month"], cell["direction"])
            for cell in audit.get("cells", [])
            if not cell.get("error") and cell.get("complete")
        }
        directions = set(grouped_queries())
        cursor = dt.date.today().replace(day=1)
        selected = None
        for _ in range(36):
            month_key = cursor.strftime("%Y-%m")
            if any((month_key, direction) not in covered for direction in directions):
                selected = cursor
                break
            cursor = (cursor - dt.timedelta(days=1)).replace(day=1)
        selected = selected or dt.date.today().replace(day=1)
        run([selected.year], [selected.month], args.max_per_cell)
        return
    if not args.year:
        parser.error("provide --year or use --auto")
    run(sorted(set(args.year)), sorted(set(args.month or range(1, 13))), args.max_per_cell)


if __name__ == "__main__":
    main()
