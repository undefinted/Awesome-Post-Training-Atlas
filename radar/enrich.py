from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import yaml

from radar.main import ARXIV_API, ATOM, ROOT, load_yaml, normalize_arxiv_id, urlopen_with_retry


S2_PAPER_BATCH = "https://api.semanticscholar.org/graph/v1/paper/batch"
S2_AUTHOR_BATCH = "https://api.semanticscholar.org/graph/v1/author/batch"


def fetch_arxiv_ids(ids: list[str]) -> dict[str, dict]:
    output = {}
    for offset in range(0, len(ids), 40):
        bare = [paper_id.split(":", 1)[1] for paper_id in ids[offset : offset + 40]]
        params = urllib.parse.urlencode({"id_list": ",".join(bare), "max_results": len(bare)})
        request = urllib.request.Request(f"{ARXIV_API}?{params}", headers={"User-Agent": "Awesome-Post-Training-Atlas/0.3"})
        with urlopen_with_retry(request) as response:
            root = ET.fromstring(response.read())
        for entry in root.findall("atom:entry", ATOM):
            paper_id = normalize_arxiv_id(entry.findtext("atom:id", "", ATOM))
            output[paper_id] = {
                "authors": [node.findtext("atom:name", "", ATOM) for node in entry.findall("atom:author", ATOM)]
            }
    return output


def post_json(url: str, body: dict, fields: str) -> list:
    request = urllib.request.Request(
        f"{url}?{urllib.parse.urlencode({'fields': fields})}",
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "Awesome-Post-Training-Atlas/0.3"},
    )
    if os.getenv("SEMANTIC_SCHOLAR_API_KEY"):
        request.add_header("x-api-key", os.environ["SEMANTIC_SCHOLAR_API_KEY"])
    with urlopen_with_retry(request, timeout=90) as response:
        return json.loads(response.read())


def enrich_academic_metadata(papers: list[dict], include_institutions: bool = True) -> None:
    arxiv_ids = [paper["id"] for paper in papers if paper["id"].startswith("arxiv:")]
    if not arxiv_ids:
        return
    s2_papers = []
    for offset in range(0, len(arxiv_ids), 400):
        s2_papers.extend(
            post_json(
                S2_PAPER_BATCH,
                {"ids": [paper_id.upper() for paper_id in arxiv_ids[offset : offset + 400]]},
                "externalIds,authors,venue,publicationVenue,journal,year",
            )
        )
    profiles = {}
    if include_institutions:
        author_ids = sorted(
            {author["authorId"] for paper in s2_papers if paper for author in paper.get("authors", []) if author.get("authorId")}
        )
        for offset in range(0, len(author_ids), 1000):
            batch = post_json(S2_AUTHOR_BATCH, {"ids": author_ids[offset : offset + 1000]}, "name,affiliations")
            profiles.update({author["authorId"]: author for author in batch if author})
    by_arxiv = {}
    for record in s2_papers:
        if not record:
            continue
        arxiv_id = (record.get("externalIds") or {}).get("ArXiv")
        if arxiv_id:
            by_arxiv[f"arxiv:{arxiv_id.lower()}"] = record
    checked_at = dt.datetime.now(dt.timezone.utc).isoformat()
    for paper in papers:
        record = by_arxiv.get(paper["id"].lower())
        if include_institutions:
            institutions = sorted(
                {
                    affiliation
                    for author in (record or {}).get("authors", [])
                    for affiliation in profiles.get(author.get("authorId"), {}).get("affiliations", [])
                    if affiliation
                }
            )
            if institutions:
                paper["institutions"] = institutions
                paper["institution_source"] = "semantic-scholar-author-profiles"
                paper["institution_note"] = "Author-profile affiliations; may differ from publication-time affiliations."
            paper["institution_enrichment_checked_at"] = checked_at
        publication_venue = (record or {}).get("publicationVenue") or {}
        venue_name = publication_venue.get("name") or (record or {}).get("venue")
        if venue_name and venue_name.strip().lower() not in {"arxiv", "arxiv.org", "corr"}:
            paper["venue"] = venue_name.strip()
            paper["venue_type"] = publication_venue.get("type") or "publication venue"
            if publication_venue.get("url"):
                paper["venue_url"] = publication_venue["url"]
            paper["venue_source"] = "semantic-scholar-paper-metadata"
        paper["venue_enrichment_checked_at"] = checked_at


def enrich_file(path, include_authors: bool, include_institutions: bool, limit: int | None = None) -> int:
    papers = load_yaml(path)["papers"]
    selected = [paper for paper in papers if paper["id"].startswith("arxiv:")]
    refresh_before = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=14)
    selected = [
        paper
        for paper in selected
        if not paper.get("venue_enrichment_checked_at")
        or (
            not paper.get("venue")
            and dt.datetime.fromisoformat(paper["venue_enrichment_checked_at"]) <= refresh_before
        )
    ]
    selected = selected[:limit] if limit else selected
    if include_authors:
        arxiv_ids = [paper["id"] for paper in selected]
        metadata = fetch_arxiv_ids(arxiv_ids)
        for paper in selected:
            record = metadata.get(paper["id"].lower())
            if record and record.get("authors"):
                paper["authors"] = record["authors"]
                paper["author_source"] = "arxiv"
    try:
        enrich_academic_metadata(selected, include_institutions)
    except Exception as exc:
        print(f"Semantic Scholar enrichment skipped: {type(exc).__name__}: {str(exc).encode('ascii', 'backslashreplace').decode('ascii')}")
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump({"papers": papers}, handle, sort_keys=False, allow_unicode=True, width=120)
    return len(selected)


def enrich_curated(include_institutions: bool = True) -> None:
    path = ROOT / "data" / "papers.yaml"
    papers = load_yaml(path)["papers"]
    arxiv_ids = [paper["id"] for paper in papers if paper["id"].startswith("arxiv:")]
    metadata = fetch_arxiv_ids(arxiv_ids)
    for paper in papers:
        record = metadata.get(paper["id"].lower())
        if record and record.get("authors"):
            paper["authors"] = record["authors"]
            paper["author_source"] = "arxiv"
    try:
        enrich_academic_metadata(papers, include_institutions)
    except Exception as exc:
        print(f"Semantic Scholar enrichment skipped: {type(exc).__name__}: {str(exc).encode('ascii', 'backslashreplace').decode('ascii')}")
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump({"papers": papers}, handle, sort_keys=False, allow_unicode=True, width=120)


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich records with sourced academic author and institution metadata")
    parser.add_argument("--no-institutions", action="store_true")
    parser.add_argument("--include-candidates", action="store_true")
    parser.add_argument("--candidate-limit", type=int, default=500)
    args = parser.parse_args()
    enrich_curated(not args.no_institutions)
    if args.include_candidates:
        count = enrich_file(
            ROOT / "data" / "candidates.yaml",
            include_authors=False,
            include_institutions=not args.no_institutions,
            limit=args.candidate_limit,
        )
        print(f"Checked institution and publication-venue metadata for {count} discovery candidates")


if __name__ == "__main__":
    main()
