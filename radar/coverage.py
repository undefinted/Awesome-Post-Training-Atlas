from __future__ import annotations

import argparse
import datetime as dt
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
START = "<!-- COVERAGE:START -->"
END = "<!-- COVERAGE:END -->"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def month_range(start: str, end: str):
    year, month = map(int, start.split("-"))
    end_year, end_month = map(int, end.split("-"))
    while (year, month) <= (end_year, end_month):
        yield f"{year:04d}-{month:02d}"
        month += 1
        if month == 13:
            year += 1
            month = 1


def render_coverage(since: str = "2024-01") -> str:
    directions = load_yaml(ROOT / "config" / "taxonomy.yaml")["directions"]
    papers = load_yaml(ROOT / "data" / "papers.yaml")["papers"]
    current = dt.date.today().strftime("%Y-%m")
    counts = Counter((str(paper["date"])[:7], paper["direction"]) for paper in papers)
    short = {item["id"]: item["id"].replace("-", " ") for item in directions}
    ids = [item["id"] for item in directions]
    lines = [
        f"Coverage window: **{since} through {current}**.",
        "",
        "| Month | " + " | ".join(short[item] for item in ids) + " | Total |",
        "|---|" + "---:|" * (len(ids) + 1),
    ]
    for month in reversed(list(month_range(since, current))):
        values = [counts[(month, direction)] for direction in ids]
        lines.append(f"| {month} | " + " | ".join(map(str, values)) + f" | **{sum(values)}** |")
    lines.extend(
        [
            "",
            "Direction IDs are defined in [TAXONOMY.md](TAXONOMY.md). The Backfill Agent prioritizes recent empty or thin months while preserving the inclusion policy.",
            "",
        ]
    )
    return "\n".join(lines)


def update(check: bool = False) -> None:
    path = ROOT / "COVERAGE.md"
    original = path.read_text(encoding="utf-8")
    before, remainder = original.split(START, 1)
    _, after = remainder.split(END, 1)
    updated = f"{before}{START}\n{render_coverage()}{END}{after}"
    if check and updated != original:
        raise SystemExit("COVERAGE.md is stale; run python -m radar.coverage")
    if not check:
        path.write_text(updated, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    update(check=args.check)


if __name__ == "__main__":
    main()

