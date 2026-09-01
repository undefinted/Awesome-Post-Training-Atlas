from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DIRECTIONS_DIR = ROOT / "directions"
START = "<!-- PAPERS:START -->"
END = "<!-- PAPERS:END -->"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def all_records() -> list[dict]:
    curated = [dict(paper) for paper in load_yaml(ROOT / "data" / "papers.yaml")["papers"]]
    known = {paper["id"].lower() for paper in curated}
    candidates_path = ROOT / "data" / "candidates.yaml"
    candidates = (load_yaml(candidates_path) or {}).get("papers", []) if candidates_path.exists() else []
    for source in candidates:
        if source["id"].lower() in known:
            continue
        candidate = dict(source)
        candidate["direction"] = (
            candidate.get("direction")
            or candidate.get("suggested_direction")
            or (candidate.get("direction_hints") or ["needs-review"])[0]
        )
        candidate["discovery_candidate"] = True
        curated.append(candidate)
    return curated


def render_papers(records: list[dict], year_level: int = 2) -> str:
    sections: list[str] = []
    years = sorted({str(paper["date"])[:4] for paper in records}, reverse=True)
    for year in years:
        sections.append(f"{'#' * year_level} {year}\n")
        by_year = [paper for paper in records if str(paper["date"]).startswith(year)]
        months = sorted({str(paper["date"])[5:7] for paper in by_year}, reverse=True)
        for month in months:
            month_name = dt.date(2000, int(month), 1).strftime("%B")
            sections.append(f"{'#' * (year_level + 1)} {month_name}\n")
            by_month = sorted(
                [paper for paper in by_year if str(paper["date"])[5:7] == month],
                key=lambda paper: str(paper["date"]),
                reverse=True,
            )
            for paper in by_month:
                if paper.get("discovery_candidate"):
                    sources = ", ".join(paper.get("source_signals", ["academic-search"]))
                    sections.append(
                        f"- 🔎 **[{paper['title']}]({paper['url']})** — `discovery candidate`; awaiting primary-paper curation.  \n"
                        f"  {str(paper['date'])} · `{paper.get('classification_method', 'query-hint')}` · `{sources}`\n"
                    )
                else:
                    tags = " · ".join(f"`{tag}`" for tag in paper.get("tags", []))
                    code = f" · [code]({paper['code']})" if paper.get("code") else ""
                    sections.append(
                        f"- **[{paper['title']}]({paper['url']})** — {paper['key_idea']}  \n"
                        f"  {str(paper['date'])} · {tags}{code}\n"
                    )
    return "\n".join(sections).rstrip() + "\n"


def direction_page(direction: dict, records: list[dict]) -> str:
    selected = [paper for paper in records if paper["direction"] == direction["id"]]
    curated_count = sum(not paper.get("discovery_candidate") for paper in selected)
    candidate_count = len(selected) - curated_count
    return (
        f"# {direction['title']}\n\n"
        "[← Back to the atlas](../README.md)\n\n"
        f"**{len(selected)} papers**: {curated_count} curated and {candidate_count} academic discovery candidates.\n\n"
        "Curated entries include a reviewed key idea and tags. 🔎 entries were found directly through academic search and remain visibly provisional until primary-paper review.\n\n"
        f"{render_papers(selected)}"
    )


def render_index(taxonomy: list[dict], records: list[dict]) -> str:
    lines = [
        "## Research directions",
        "",
        "Each direction has its own chronological page. Counts include curated papers and visibly marked academic discovery candidates.",
        "",
        "| Direction | Curated | Discovery | Total | Latest |",
        "|---|---:|---:|---:|---:|",
    ]
    for direction in taxonomy:
        selected = [paper for paper in records if paper["direction"] == direction["id"]]
        curated_count = sum(not paper.get("discovery_candidate") for paper in selected)
        candidate_count = len(selected) - curated_count
        latest = max((str(paper["date"]) for paper in selected), default="—")
        lines.append(
            f"| [{direction['title']}](directions/{direction['id']}.md) | {curated_count} | {candidate_count} | **{len(selected)}** | {latest} |"
        )
    return "\n".join(lines) + "\n"


def update_readme(check: bool = False) -> bool:
    taxonomy = load_yaml(ROOT / "config" / "taxonomy.yaml")["directions"]
    records = all_records()
    path = ROOT / "README.md"
    original = path.read_text(encoding="utf-8")
    before, remainder = original.split(START, 1)
    _, after = remainder.split(END, 1)
    updated = f"{before}{START}\n{render_index(taxonomy, records)}{END}{after}"
    changed = updated != original
    expected_pages = {
        DIRECTIONS_DIR / f"{direction['id']}.md": direction_page(direction, records)
        for direction in taxonomy
    }
    stale_pages = [page for page, content in expected_pages.items() if not page.exists() or page.read_text(encoding="utf-8") != content]
    if check and (changed or stale_pages):
        raise SystemExit("README or direction pages are stale; run python -m radar.render")
    if not check:
        path.write_text(updated, encoding="utf-8", newline="\n")
        DIRECTIONS_DIR.mkdir(exist_ok=True)
        for page, content in expected_pages.items():
            page.write_text(content, encoding="utf-8", newline="\n")
    return changed or bool(stale_pages)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    update_readme(check=args.check)


if __name__ == "__main__":
    main()

