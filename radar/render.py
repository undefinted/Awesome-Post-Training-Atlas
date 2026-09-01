from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
START = "<!-- PAPERS:START -->"
END = "<!-- PAPERS:END -->"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def render_index() -> str:
    taxonomy = load_yaml(ROOT / "config" / "taxonomy.yaml")["directions"]
    papers = load_yaml(ROOT / "data" / "papers.yaml")["papers"]
    sections: list[str] = []
    for direction in taxonomy:
        selected = [paper for paper in papers if paper["direction"] == direction["id"]]
        if not selected:
            continue
        sections.append(f"## {direction['title']}\n")
        years = sorted({str(paper["date"])[:4] for paper in selected}, reverse=True)
        for year in years:
            sections.append(f"### {year}\n")
            by_year = [paper for paper in selected if str(paper["date"]).startswith(year)]
            months = sorted({str(paper["date"])[5:7] for paper in by_year}, reverse=True)
            for month in months:
                month_name = dt.date(2000, int(month), 1).strftime("%B")
                sections.append(f"#### {month_name}\n")
                by_month = sorted(
                    [paper for paper in by_year if str(paper["date"])[5:7] == month],
                    key=lambda paper: str(paper["date"]),
                    reverse=True,
                )
                for paper in by_month:
                    tags = " · ".join(f"`{tag}`" for tag in paper.get("tags", []))
                    code = f" · [code]({paper['code']})" if paper.get("code") else ""
                    sections.append(
                        f"- **[{paper['title']}]({paper['url']})** — {paper['key_idea']}  \n"
                        f"  {str(paper['date'])} · {tags}{code}\n"
                    )
    return "\n".join(sections).rstrip() + "\n"


def update_readme(check: bool = False) -> bool:
    path = ROOT / "README.md"
    original = path.read_text(encoding="utf-8")
    before, remainder = original.split(START, 1)
    _, after = remainder.split(END, 1)
    updated = f"{before}{START}\n{render_index()}{END}{after}"
    changed = updated != original
    if check and changed:
        raise SystemExit("README paper index is stale; run python -m radar.render")
    if not check:
        path.write_text(updated, encoding="utf-8", newline="\n")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    update_readme(check=args.check)


if __name__ == "__main__":
    main()

