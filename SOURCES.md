# Sources and freshness policy

The atlas separates primary research evidence from discovery and community
signals. Popularity can influence review priority, but never inclusion by
itself.

## Daily sources

| Source | Role | Target latency | Stored signal |
|---|---|---:|---|
| arXiv | Primary preprint discovery | 24–48 hours | ID, title, abstract, date, categories |
| Hugging Face Daily Papers | Community prioritization and code discovery | 24 hours | upvotes, discussion page, repository |
| OpenReview | Conference submission and review signal | 1–7 days | forum, venue, decision/review state |
| Semantic Scholar | Metadata enrichment and version matching | 1–7 days | DOI, venue, citations, external IDs |
| GitHub | Implementation verification | 1–7 days | official repository and activity |

The repository-native Daily Radar fetches arXiv and Hugging Face every day.
The Weekly Backfill Radar queries arXiv directly, walks older result pages with
persistent per-query cursors, and records its exact date window, offsets, and
result counts. OpenReview and Semantic Scholar are used to resolve conference
status, versions, and citation relations during curation.

## Historical cross-checks

Third-party awesome lists are not ingestion sources, do not increase a paper's
score, and are not cited as research evidence. They may be used manually only
as a recall audit: if they reveal a possible omission, the Agent must rediscover
and verify the work through arXiv, OpenReview, a publisher page, or an official
author project page before it enters any candidate queue.

The generated `DISCOVERY_COVERAGE.md` summarizes the academic search. Exact
queries and counts live in `data/search_audit.yaml`; resumable pagination
offsets live in `data/search_cursors.yaml`.

## Community sources

Publicly searchable posts from research blogs, newsletters, X/Twitter,
Reddit, Hacker News, 知乎, 微信公众号, and 小红书 may be recorded in
`data/community_signals.yaml` when they add one of the following:

- an original explanation or reproduction;
- evidence of unusual practitioner interest;
- a correction, limitation, or failed reproduction;
- a useful connection between papers or methods.

Every record must include its URL, discovery date, source, a neutral summary,
and the paper/project IDs it discusses. Community content is kept separate
from `data/papers.yaml`, and promotional reposts are excluded.

## Time organization

- Candidate pull requests are daily and grouped by exact date.
- The main atlas is grouped by direction, year, and month.
- Monthly synthesis notes summarize accepted work, technique changes, and
  recurring community signals; they do not merely repeat paper titles.
