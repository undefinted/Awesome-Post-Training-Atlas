from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DIRECTIONS_DIR = ROOT / "directions"
START = "<!-- PAPERS:START -->"
END = "<!-- PAPERS:END -->"
LABELS_OUTPUT = ROOT / "LABELS.md"


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


def render_papers(
    records: list[dict],
    year_level: int = 2,
    month_keys: list[str] | None = None,
    audit: dict[str, dict] | None = None,
) -> str:
    from radar.labels import effective_labels, label_index

    label_names = {key: value["title"] for key, value in label_index().items()}
    sections: list[str] = []
    audit = audit or {}
    month_keys = month_keys or sorted({str(paper["date"])[:7] for paper in records}, reverse=True)
    years = sorted({month[:4] for month in month_keys}, reverse=True)
    for year in years:
        sections.append(f"<a id=\"{year}\"></a>\n\n{'#' * year_level} {year}\n")
        by_year = [paper for paper in records if str(paper["date"]).startswith(year)]
        months = [month_key[5:7] for month_key in month_keys if month_key.startswith(year)]
        for month in months:
            month_key = f"{year}-{month}"
            month_name = dt.date(2000, int(month), 1).strftime("%B")
            sections.append(f"<a id=\"{year}-{month}\"></a>\n\n{'#' * (year_level + 1)} {month_name}\n")
            by_month = sorted(
                [paper for paper in by_year if str(paper["date"])[5:7] == month],
                key=lambda paper: str(paper["date"]),
                reverse=True,
            )
            cell = audit.get(month_key)
            if not cell:
                sections.append(
                    "> **Audit status:** ⏳ Not audited yet. No completeness claim is made for this direction-month cell.\n"
                )
            elif cell.get("error"):
                sections.append(
                    f"> **Audit status:** ⚠ Failed — `{cell['error']}` · checked {cell.get('checked_at', 'time unavailable')}.\n"
                )
            elif cell.get("complete"):
                sections.append(
                    f"> **Audit status:** ✓ Complete · scanned {cell.get('records_scanned', 0)} academic records · "
                    f"{cell.get('eligible', 0)} eligible · checked {cell.get('checked_at', 'time unavailable')}.\n"
                )
            else:
                sections.append(
                    f"> **Audit status:** ◐ Incomplete or truncated · scanned {cell.get('records_scanned', 0)} academic records · "
                    f"{cell.get('eligible', 0)} eligible · checked {cell.get('checked_at', 'time unavailable')}.\n"
                )
            if not by_month:
                sections.append("_No visible paper records in this cell yet._\n")
            for paper in by_month:
                labels = " · ".join(f"`{label_names[label]}`" for label in effective_labels(paper))
                if paper.get("discovery_candidate"):
                    sources = ", ".join(paper.get("source_signals", ["academic-search"]))
                    authors = ", ".join(paper.get("authors", [])[:8])
                    if len(paper.get("authors", [])) > 8:
                        authors += ", et al."
                    institutions = "; ".join(paper.get("institutions", [])[:5])
                    venue = paper.get("venue")
                    venue_link = f"[{venue}]({paper['venue_url']})" if venue and paper.get("venue_url") else venue
                    sections.append(
                        f"- 🔎 **[{paper['title']}]({paper['url']})** — `discovery candidate`; awaiting primary-paper curation.  \n"
                        f"  {str(paper['date'])} · `{paper.get('classification_method', 'query-hint')}` · `{sources}`  \n"
                        f"  Labels: {labels or 'pending'}  \n"
                        f"  Authors: {authors or 'metadata pending'}"
                        + (f"  \n  Institutions*: {institutions}" if institutions else "")
                        + (f"  \n  Venue: {venue_link}" if venue_link else "")
                        + "\n"
                    )
                else:
                    tags = " · ".join(f"`{tag}`" for tag in paper.get("tags", []))
                    code = f" · [code]({paper['code']})" if paper.get("code") else ""
                    authors = ", ".join(paper.get("authors", [])[:8])
                    if len(paper.get("authors", [])) > 8:
                        authors += ", et al."
                    institutions = "; ".join(paper.get("institutions", [])[:5])
                    venue = paper.get("venue")
                    venue_link = f"[{venue}]({paper['venue_url']})" if venue and paper.get("venue_url") else venue
                    sections.append(
                        f"- **[{paper['title']}]({paper['url']})** — {paper['key_idea']}  \n"
                        f"  {str(paper['date'])} · {tags}{code}  \n"
                        f"  Labels: {labels or 'pending'}  \n"
                        f"  Authors: {authors or 'metadata pending'}"
                        + (f"  \n  Institutions*: {institutions}" if institutions else "")
                        + (f"  \n  Venue: {venue_link}" if venue_link else "")
                        + "\n"
                    )
    return "\n".join(sections).rstrip() + "\n"


def direction_page(direction: dict, records: list[dict]) -> str:
    selected = [paper for paper in records if paper["direction"] == direction["id"]]
    curated_count = sum(not paper.get("discovery_candidate") for paper in selected)
    candidate_count = len(selected) - curated_count
    audit_path = ROOT / "data" / "monthly_audit.yaml"
    audit_cells = (load_yaml(audit_path) or {"cells": []})["cells"] if audit_path.exists() else []
    audit = {cell["month"]: cell for cell in audit_cells if cell["direction"] == direction["id"]}
    latest_complete_month = (dt.date.today().replace(day=1) - dt.timedelta(days=1)).replace(day=1)
    dense_months = []
    cursor = dt.date(2024, 1, 1)
    while cursor <= latest_complete_month:
        dense_months.append(cursor.strftime("%Y-%m"))
        cursor = (cursor.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    existing_months = {str(paper["date"])[:7] for paper in selected}
    displayed_months = sorted(set(dense_months) | existing_months, reverse=True)
    years = sorted({month[:4] for month in displayed_months}, reverse=True)
    directory = []
    for year in years:
        month_items = []
        for month_key in [month for month in displayed_months if month.startswith(year)]:
            month = month_key[5:7]
            month_name = dt.date(2000, int(month), 1).strftime("%b")
            count = sum(str(paper["date"]).startswith(month_key) for paper in selected)
            cell = audit.get(month_key)
            if count:
                state = "✓" if cell and cell.get("complete") and not cell.get("error") else "◐"
                month_items.append(f"[{month_name}](#{month_key}) {state}{count}")
            elif cell and cell.get("complete") and not cell.get("error"):
                month_items.append(f"[{month_name}](#{month_key}) ✓0")
            elif cell and (cell.get("error") or not cell.get("complete")):
                month_items.append(f"[{month_name}](#{month_key}) ⚠")
            else:
                month_items.append(f"[{month_name}](#{month_key}) ⏳")
        directory.append(f"- [{year}](#{year}) — " + " · ".join(month_items))
    return (
        f"# {direction['title']}\n\n"
        "[← Back to the atlas](../README.md)\n\n"
        f"**{len(selected)} papers**: {curated_count} curated and {candidate_count} academic discovery candidates.\n\n"
        "Curated entries include a reviewed key idea and tags. 🔎 entries were found directly through academic search and remain visibly provisional until primary-paper review.\n\n"
        "*Institution names, when shown, come from Semantic Scholar author profiles and may differ from affiliations at publication time.*\n\n"
        "## Monthly audit directory\n\n"
        "`✓N` audited with N visible records · `✓0` audited with no eligible record · `◐N` records exist but the month audit is incomplete · `⏳` not audited · `⚠` failed or truncated.\n\n"
        + "\n".join(directory)
        + "\n\n"
        + render_papers(selected, month_keys=displayed_months, audit=audit)
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


def render_label_catalog(records: list[dict]) -> str:
    from radar.labels import effective_labels, vocabulary

    counts = {label["id"]: 0 for label in vocabulary()}
    for paper in records:
        for label in effective_labels(paper):
            counts[label] += 1
    lines = [
        "# Controlled label directory",
        "",
        "[← Back to the atlas](README.md) · [Open interactive filters](https://undefinted.github.io/Awesome-Post-Training-Atlas/)",
        "",
        "Labels are extracted reproducibly from title, abstract, reviewed key idea, and existing tags. Counts include curated and provisional academic-discovery records.",
        "",
        "| Category | Label | Papers | Definition |",
        "|---|---|---:|---|",
    ]
    for label in sorted(vocabulary(), key=lambda item: (item["category"], item["title"].lower())):
        lines.append(f"| {label['category']} | `{label['title']}` | {counts[label['id']]} | {label['description']} |")
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
    expected_pages[LABELS_OUTPUT] = render_label_catalog(records)
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
