"""Real-time Xiaohongshu (RED) technical-keyword scanner.

Xiaohongshu has no public search API, so this module queries public web
search engines (Bing and DuckDuckGo's HTML endpoint) for note-level
xiaohongshu.com URLs matching the atlas's technical keywords, then records
qualifying notes as community signals in data/community_signals.yaml
following the policy in SOURCES.md.

Design rules inherited from the rest of the radar:

- works without any API key or login;
- every backend failure is non-fatal (a warning on stderr, zero signals);
- reruns are idempotent: signal IDs derive from the canonical note URL;
- promotional reposts are excluded (SOURCES.md community policy).

CLI examples:

    python -m radar.xiaohongshu                     # scan configured keywords, merge into YAML
    python -m radar.xiaohongshu --dry-run           # live scan, print, write nothing
    python -m radar.xiaohongshu --keyword GRPO --dry-run --json
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

from radar.main import ROOT, load_yaml, strip_markup, urlopen_with_retry


# Search engines reject the project-style user agent used for academic APIs;
# a plain browser UA is required for their public HTML result pages.
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

BING_SEARCH = "https://www.bing.com/search"
DDG_SEARCH = "https://html.duckduckgo.com/html/"

# Note-level Xiaohongshu pages. Homepages, topic pages, and user profiles are
# not community signals: a signal must point at one specific note.
NOTE_PATH = re.compile(r"^/(?:explore|discovery/item)/([0-9A-Za-z]{10,})(?:/)?$")

# arXiv identifiers mentioned inside note titles/snippets (new style only).
ARXIV_IN_TEXT = re.compile(r"(?<![\d.])(\d{4}\.\d{4,5})(?:v\d+)?(?![\d.])")

# DuckDuckGo wraps outbound links in a redirect endpoint.
DDG_REDIRECT_HOSTS = {"duckduckgo.com", "www.duckduckgo.com"}

DEFAULT_EXCLUDE_TERMS = [
    "加微信",
    "+v",
    "优惠券",
    "代购",
    "点赞关注",
    "评论区领取",
    "资料包",
    "训练营",
    "课程链接",
    "私信领取",
    "免费送",
]

CHINA_STANDARD_TIME = dt.timezone(dt.timedelta(hours=8))


def canonical_note_url(url: str) -> str | None:
    """Normalize a Xiaohongshu note URL, dropping tracking parameters.

    Returns None for non-Xiaohongshu URLs and for non-note pages such as the
    homepage, topic pages, or user profiles.
    """
    if not url:
        return None
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return None
    host = parts.netloc.lower().split(":", 1)[0]
    if host not in {"xiaohongshu.com", "www.xiaohongshu.com"}:
        return None
    match = NOTE_PATH.match(parts.path)
    if not match:
        return None
    return f"https://www.xiaohongshu.com/explore/{match.group(1).lower()}"


def resolve_result_url(href: str) -> str | None:
    """Resolve a search-result href to its destination URL.

    DuckDuckGo encodes destinations in the uddg parameter of a redirect URL;
    Bing uses direct hrefs. Returns None for unresolvable hrefs.
    """
    if not href:
        return None
    if href.startswith("//"):
        href = f"https:{href}"
    try:
        parts = urllib.parse.urlsplit(href)
    except ValueError:
        return None
    host = parts.netloc.lower().split(":", 1)[0]
    if host in DDG_REDIRECT_HOSTS and parts.path.startswith("/l/"):
        wrapped = urllib.parse.parse_qs(parts.query).get("uddg", [None])[0]
        return urllib.parse.unquote(wrapped) if wrapped else None
    if parts.scheme in {"http", "https"}:
        return href
    return None


def _strip(value: str) -> str:
    return " ".join(strip_markup(value).split())


def parse_bing_results(html: str) -> list[dict]:
    """Parse Bing's public HTML results into {url, title, snippet} hits."""
    hits = []
    for block in re.split(r'<li class="b_algo"', html)[1:]:
        title_match = re.search(r'<h2[^>]*>\s*<a[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', block, re.S)
        if not title_match:
            continue
        url = resolve_result_url(title_match.group(1))
        title = _strip(title_match.group(2))
        snippet_match = re.search(r'<p class="b_lineclamp[^"]*"[^>]*>(.*?)</p>', block, re.S) or re.search(
            r"<p[^>]*>(.*?)</p>", block, re.S
        )
        snippet = _strip(snippet_match.group(1)) if snippet_match else ""
        if url and title:
            hits.append({"url": url, "title": title, "snippet": snippet})
    return hits


def parse_duckduckgo_results(html: str) -> list[dict]:
    """Parse DuckDuckGo's HTML endpoint results into {url, title, snippet} hits."""
    hits = []
    for block in re.split(r'<div class="result results_links', html)[1:]:
        title_match = re.search(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, re.S)
        if not title_match:
            continue
        url = resolve_result_url(title_match.group(1))
        title = _strip(title_match.group(2))
        snippet_match = re.search(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', block, re.S)
        snippet = _strip(snippet_match.group(1)) if snippet_match else ""
        if url and title:
            hits.append({"url": url, "title": title, "snippet": snippet})
    return hits


def _freshness_bucket(days: int) -> str | None:
    if days <= 1:
        return "day"
    if days <= 7:
        return "week"
    if days <= 31:
        return "month"
    return None


def bing_search_url(query: str, freshness_days: int, count: int) -> str:
    params: dict[str, str | int] = {"q": query, "count": max(1, min(int(count), 30)), "setlang": "zh-CN"}
    bucket = _freshness_bucket(freshness_days)
    if bucket:
        params["filters"] = 'ex1:"' + {"day": "ez1", "week": "ez2", "month": "ez3"}[bucket] + '"'
    return f"{BING_SEARCH}?{urllib.parse.urlencode(params)}"


def duckduckgo_search_url(query: str, freshness_days: int) -> str:
    params: dict[str, str] = {"q": query}
    bucket = _freshness_bucket(freshness_days)
    if bucket:
        params["df"] = {"day": "d", "week": "w", "month": "m"}[bucket]
    return f"{DDG_SEARCH}?{urllib.parse.urlencode(params)}"


BACKENDS = {
    "bing": (bing_search_url, parse_bing_results),
    "duckduckgo": (duckduckgo_search_url, parse_duckduckgo_results),
}


def fetch_html(url: str, timeout: int) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": BROWSER_UA,
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urlopen_with_retry(request, timeout=timeout, attempts=2) as response:
        return response.read().decode("utf-8", errors="replace")


def search_keyword(keyword: str, config: dict, backends: list[str]) -> tuple[list[dict], str | None, list[str]]:
    """Query each backend in order; return hits from the first yielding notes.

    Returns (hits, backend_name_or_None, backends_that_failed).
    """
    template = config.get("query_template", 'site:xiaohongshu.com "{keyword}"')
    query = template.format(keyword=keyword)
    freshness = int(config.get("freshness_days", 31))
    timeout = int(config.get("timeout_seconds", 30))
    fallback: list[dict] = []
    failed: list[str] = []
    for name in backends:
        if name not in BACKENDS:
            print(f"Warning: unknown Xiaohongshu search backend {name!r}; skipping.", file=sys.stderr)
            continue
        url_builder, parser = BACKENDS[name]
        if name == "bing":
            url = url_builder(query, freshness, int(config.get("max_results_per_keyword", 10)) + 10)
        else:
            url = url_builder(query, freshness)
        try:
            html = fetch_html(url, timeout)
        except Exception as exc:
            # A blocked or throttled search backend must not fail the scan of
            # the remaining keywords or the rest of the daily radar.
            print(f"Warning: Xiaohongshu search via {name} failed for {keyword!r}: {exc}", file=sys.stderr)
            failed.append(name)
            continue
        hits = parser(html)
        if any(canonical_note_url(hit["url"]) for hit in hits):
            return hits, name, failed
        # Keep the largest non-note page as a fallback so a backend that only
        # surfaces Xiaohongshu's homepage still counts as "answered".
        if len(hits) > len(fallback):
            fallback = hits
    return fallback, None, failed


def extract_arxiv_ids(text: str) -> list[str]:
    ids = {f"arxiv:{match.group(1)}" for match in ARXIV_IN_TEXT.finditer(text or "")}
    return sorted(ids)


def is_promotional(text: str, exclude_terms: list[str]) -> bool:
    lowered = (text or "").lower()
    return any(term.lower() in lowered for term in exclude_terms)


def collect_note_hits(keyword: str, hits: list[dict], config: dict) -> list[dict]:
    """Filter raw search hits down to qualifying Xiaohongshu notes."""
    exclude_terms = list(config.get("exclude_terms") or DEFAULT_EXCLUDE_TERMS)
    limit = int(config.get("max_results_per_keyword", 10))
    notes = []
    seen = set()
    for hit in hits:
        canonical = canonical_note_url(hit["url"])
        if not canonical or canonical in seen:
            continue
        text = f"{hit['title']} {hit['snippet']}"
        if is_promotional(text, exclude_terms):
            continue
        seen.add(canonical)
        notes.append({**hit, "url": canonical, "keyword": keyword})
        if len(notes) >= limit:
            break
    return notes


def signal_id_for(url: str) -> str:
    note_id = url.rstrip("/").rsplit("/", 1)[-1]
    if re.fullmatch(r"[0-9a-z]{10,}", note_id):
        return f"community:xiaohongshu-{note_id}"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    return f"community:xiaohongshu-{digest}"


def build_signal(hit: dict, today: dt.date) -> dict:
    text = f"{hit['title']} {hit['snippet']}".strip()
    summary = 'A Xiaohongshu note titled "' + hit["title"] + '" matched the technical keyword "' + hit["keyword"] + '".'
    if hit.get("snippet"):
        summary += ' Search snippet: "' + hit["snippet"][:200] + '"'
    signal = {
        "id": signal_id_for(hit["url"]),
        "date": today,
        "source": "xiaohongshu",
        "url": hit["url"],
        "summary": summary,
        "related_ids": extract_arxiv_ids(text),
        "keyword": hit["keyword"],
    }
    if hit.get("direction"):
        signal["direction_hint"] = hit["direction"]
    return signal


def merge_signals(existing: list[dict], new_signals: list[dict], max_stored: int) -> tuple[list[dict], int]:
    """Merge new signals into the store.

    Existing records keep their position and original discovery date; new
    records are appended. When Xiaohongshu-sourced records exceed
    max_stored, the oldest ones (by discovery date) are pruned; records from
    other sources are never pruned. Returns (merged, added_count).
    """
    by_id = {str(signal.get("id")): signal for signal in existing}
    added = 0
    for signal in new_signals:
        if signal["id"] not in by_id:
            by_id[signal["id"]] = signal
            added += 1
    merged = list(by_id.values())
    xhs = [signal for signal in merged if signal.get("source") == "xiaohongshu"]
    if len(xhs) > max_stored:
        xhs_sorted = sorted(xhs, key=lambda signal: (str(signal.get("date", "")), str(signal.get("id", ""))))
        prune = {signal["id"] for signal in xhs_sorted[: len(xhs) - max_stored]}
        merged = [signal for signal in merged if signal["id"] not in prune]
    return merged, added


class _IndentedDumper(yaml.SafeDumper):
    """Emit block sequences indented under their mapping key (matches the
    hand-maintained style of data/community_signals.yaml)."""

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def dump_signal_entries(signals: list[dict]) -> str:
    """Render signal entries in the file's established style."""
    text = yaml.dump(
        {"signals": signals},
        Dumper=_IndentedDumper,
        sort_keys=False,
        allow_unicode=True,
        width=4096,
        default_flow_style=None,
    )
    entries = text.split("signals:\n", 1)[1]
    return entries.replace("\n  - id:", "\n\n  - id:")


def store_signals(path: Path, new_signals: list[dict], max_stored: int) -> int:
    """Merge new signals into the store file. Returns the added count.

    Existing bytes are preserved exactly: new entries are appended. A full
    rewrite happens only when the Xiaohongshu pruning cap forces one.
    """
    payload = load_yaml(path) if path.exists() else None
    existing = (payload or {}).get("signals", [])
    merged, added = merge_signals(existing, new_signals, max_stored)
    if not added:
        return 0
    if len(merged) == len(existing) + added:
        tail = merged[len(existing):]
        text = path.read_text(encoding="utf-8") if path.exists() else "signals:\n"
        if not text.endswith("\n"):
            text += "\n"
        if text.strip() in {"", "signals:"}:
            text = "signals:\n" + dump_signal_entries(tail)
        else:
            text += "\n" + dump_signal_entries(tail)
    else:
        text = "signals:\n" + dump_signal_entries(merged)
    path.write_text(text, encoding="utf-8", newline="\n")
    return added


def load_keyword_specs(config: dict) -> list[dict]:
    specs = []
    for item in config.get("keywords", []):
        if isinstance(item, str):
            specs.append({"keyword": item})
        elif isinstance(item, dict) and item.get("keyword"):
            specs.append({"keyword": str(item["keyword"]), "direction": item.get("direction")})
    return specs


def scan(config: dict, specs: list[dict], backends: list[str], max_new: int | None = None) -> list[dict]:
    """Run the live scan and return newly discovered signal records."""
    delay = float(config.get("request_delay_seconds", 4))
    today = dt.date.today()
    seen_urls: set[str] = set()
    discovered: list[dict] = []
    active = list(backends)
    consecutive_failures: dict[str, int] = {}
    for index, spec in enumerate(specs):
        if index and delay > 0:
            time.sleep(delay)
        hits, backend, failed = search_keyword(spec["keyword"], config, active)
        for name in active:
            consecutive_failures[name] = consecutive_failures.get(name, 0) + 1 if name in failed else 0
        # A backend that keeps timing out (e.g. unreachable from this network)
        # is skipped for the rest of the run so one dead endpoint cannot make
        # every keyword pay its connection timeout.
        stuck = [name for name in active if consecutive_failures.get(name, 0) >= 2]
        if stuck:
            active = [name for name in active if name not in stuck]
            print(
                f"Warning: disabling Xiaohongshu backend(s) {', '.join(stuck)} for the rest of this run after repeated failures.",
                file=sys.stderr,
            )
        notes = collect_note_hits(spec["keyword"], hits, config)
        if backend is None and not notes:
            print(f"Warning: no Xiaohongshu note results for keyword {spec['keyword']!r}.", file=sys.stderr)
        for note in notes:
            if note["url"] in seen_urls:
                continue
            seen_urls.add(note["url"])
            if spec.get("direction"):
                note["direction"] = spec["direction"]
            discovered.append(build_signal(note, today))
            if max_new is not None and len(discovered) >= max_new:
                return discovered
    return discovered


def update_status(path: Path) -> None:
    checked_at = dt.datetime.now(dt.timezone.utc).astimezone(CHINA_STANDARD_TIME).replace(microsecond=0)
    status = {}
    if path.exists():
        status = load_yaml(path) or {}
    status["last_xiaohongshu_scan_at"] = checked_at.isoformat()
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(status, handle, sort_keys=False, allow_unicode=True)


def render_hits(signals: list[dict]) -> str:
    lines = [
        "# Xiaohongshu keyword scan (live results, not stored)",
        "",
        "| Keyword | Note title | URL | arXiv refs |",
        "|---|---|---|---|",
    ]
    for signal in signals:
        summary = signal["summary"]
        title = summary.split('"')[1] if '"' in summary else summary
        title = title.replace("|", "\\|")
        refs = ", ".join(signal["related_ids"]) or "-"
        lines.append(f"| {signal['keyword']} | {title} | {signal['url']} | {refs} |")
    if not signals:
        lines.append("| - | No note-level Xiaohongshu results | - | - |")
    return "\n".join(lines)


def load_config() -> dict:
    radar = load_yaml(ROOT / "config" / "radar.yaml") or {}
    return radar.get("xiaohongshu") or {}


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan Xiaohongshu for post-training technical keywords")
    parser.add_argument("--keyword", action="append", default=[], help="Ad-hoc keyword; repeatable, replaces config keywords")
    parser.add_argument("--backend", choices=["auto", "bing", "duckduckgo"], default="auto")
    parser.add_argument("--max-results", type=int, default=None, help="Cap stored new signals for this run")
    parser.add_argument("--dry-run", action="store_true", help="Print live results without writing any file")
    parser.add_argument("--json", action="store_true", help="Emit results as JSON (implies --dry-run)")
    args = parser.parse_args()

    config = load_config()
    if args.keyword:
        specs = [{"keyword": keyword} for keyword in args.keyword]
    elif not config.get("enabled", False):
        print("Xiaohongshu scanner is disabled in config/radar.yaml; pass --keyword for an ad-hoc scan.")
        return
    else:
        specs = load_keyword_specs(config)
    if not specs:
        print("No Xiaohongshu keywords configured.")
        return

    backends = list(config.get("backends", ["bing", "duckduckgo"]))
    if args.backend != "auto":
        backends = [args.backend]
    max_new = args.max_results if args.max_results is not None else config.get("max_new_signals_per_run")
    max_new = int(max_new) if max_new else None

    signals = scan(config, specs, backends, max_new)

    if args.dry_run or args.json:
        if args.json:
            printable = [{**signal, "date": str(signal["date"])} for signal in signals]
            print(json.dumps(printable, ensure_ascii=False, indent=2))
        else:
            print(render_hits(signals))
        return

    added = store_signals(
        ROOT / "data" / "community_signals.yaml",
        signals,
        int(config.get("max_stored_signals", 200)),
    )
    update_status(ROOT / "data" / "radar_status.yaml")
    print(f"Xiaohongshu signals: +{added} new ({len(signals)} matched, {len(specs)} keywords scanned)")


if __name__ == "__main__":
    main()
