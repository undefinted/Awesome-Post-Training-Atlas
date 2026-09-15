import datetime as dt
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from radar.xiaohongshu import (
    bing_search_url,
    build_signal,
    canonical_note_url,
    collect_note_hits,
    duckduckgo_search_url,
    extract_arxiv_ids,
    is_promotional,
    merge_signals,
    parse_bing_results,
    parse_duckduckgo_results,
    resolve_result_url,
    scan,
    signal_id_for,
    store_signals,
)


# Mirrors Bing's observed markup: <li class="b_algo"> with an h2 anchor and a
# b_caption paragraph. Includes a note URL with tracking parameters, the
# Xiaohongshu homepage, a non-Xiaohongshu result, and a promotional note.
BING_FIXTURE = """
<html><body><ol id="b_results">
<li class="b_algo" data-id iid=SERP.1><div class="b_tpcn"><a class="tilk" aria-label="xiaohongshu.com"
href="https://www.xiaohongshu.com/explore/66f1a2b3c4d5e6f708192a3b?xsec_token=ABc&amp;xsec_source=pc_search">
<div class="tptxt"><div class="tptt">xiaohongshu.com</div></div></a></div>
<h2 class=""><a target="_blank" href="https://www.xiaohongshu.com/explore/66f1a2b3c4d5e6f708192a3b?xsec_token=ABc&amp;xsec_source=pc_search" h="ID=SERP,1.2"><strong>RLHF</strong> 实战笔记：奖励模型到 PPO</a></h2>
<div class="b_caption"><p class="b_lineclamp2">整理了 RLHF 全流程，并对比了 2501.12948 的 GRPO 与 2402.03300 的 DPO。</p></div></li>
<li class="b_algo"><h2 class=""><a target="_blank" href="https://www.xiaohongshu.com/" h="ID=SERP,2.1">小红书 - 你的生活兴趣社区</a></h2>
<div class="b_caption"><p class="b_lineclamp2">在小红书，分享照片和视频。</p></div></li>
<li class="b_algo"><h2><a href="https://zhuanlan.zhihu.com/p/123456789">RLHF 详解</a></h2>
<div class="b_caption"><p>知乎专栏。</p></div></li>
<li class="b_algo"><h2><a href="https://www.xiaohongshu.com/explore/67a1b2c3d4e5f60718293a4b">RLHF 资料</a></h2>
<div class="b_caption"><p>完整资料包，加微信免费领取，评论区领取链接。</p></div></li>
<li class="b_algo"><h2><a href="https://www.xiaohongshu.com/user/profile/5f0a1b2c3d4e5f60718293">某博主主页</a></h2>
<div class="b_caption"><p>用户主页。</p></div></li>
</ol></body></html>
"""

# Mirrors DuckDuckGo's html endpoint: result blocks with uddg-wrapped hrefs.
DDG_FIXTURE = """
<html><body>
<div class="result results_links results_links_deep web-result">
<h2 class="result__title"><a class="result__a" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.xiaohongshu.com%2Fexplore%2F67b1c2d3e4f60718293a4b5c%3Fxsec_token%3DXYZ&amp;rut=abc">DPO 与 GRPO 对比笔记</a></h2>
<a class="result__snippet" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.xiaohongshu.com%2Fexplore%2F67b1c2d3e4f60718293a4b5c">DPO、GRPO、PPO 三种偏好优化算法对比，参考 2402.03300。</a>
</div>
<div class="result results_links results_links_deep web-result">
<h2 class="result__title"><a class="result__a" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.com%2Fblog%2Frlhf&amp;rut=def">某英文博客</a></h2>
<a class="result__snippet" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.com%2Fblog%2Frlhf">An English blog post.</a>
</div>
</body></html>
"""

# DuckDuckGo serves this anti-bot page under automation; it must parse to zero.
DDG_CHALLENGE_FIXTURE = "<html><head><title>DuckDuckGo</title></head><body><form id=\"challenge-form\"></form></body></html>"

CONFIG = {
    "max_results_per_keyword": 10,
    "exclude_terms": ["加微信", "资料包", "评论区领取"],
}


class UrlTests(unittest.TestCase):
    def test_canonical_note_url_strips_tracking(self):
        self.assertEqual(
            canonical_note_url("https://www.xiaohongshu.com/explore/66F1A2B3C4D5E6F708192A3B?xsec_token=AB&xsec_source=pc_search"),
            "https://www.xiaohongshu.com/explore/66f1a2b3c4d5e6f708192a3b",
        )
        self.assertEqual(
            canonical_note_url("https://www.xiaohongshu.com/discovery/item/66f1a2b3c4d5e6f708192a3b"),
            "https://www.xiaohongshu.com/explore/66f1a2b3c4d5e6f708192a3b",
        )

    def test_canonical_note_url_rejects_non_note_pages(self):
        self.assertIsNone(canonical_note_url("https://www.xiaohongshu.com/"))
        self.assertIsNone(canonical_note_url("https://www.xiaohongshu.com/user/profile/5f0a1b2c3d4e5f60718293"))
        self.assertIsNone(canonical_note_url("https://www.xiaohongshu.com/search_result?keyword=RLHF"))
        self.assertIsNone(canonical_note_url("https://zhuanlan.zhihu.com/p/123"))
        self.assertIsNone(canonical_note_url("not a url"))
        self.assertIsNone(canonical_note_url(""))

    def test_resolve_result_url_unwraps_duckduckgo_redirect(self):
        wrapped = "//duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.xiaohongshu.com%2Fexplore%2F66f1a2b3c4d5e6f708192a3b%3Fxsec_token%3DAB&rut=abc"
        self.assertEqual(
            resolve_result_url(wrapped),
            "https://www.xiaohongshu.com/explore/66f1a2b3c4d5e6f708192a3b?xsec_token=AB",
        )
        self.assertEqual(resolve_result_url("https://www.xiaohongshu.com/explore/66f1a2b3c4d5e6f708192a3b"), "https://www.xiaohongshu.com/explore/66f1a2b3c4d5e6f708192a3b")
        self.assertIsNone(resolve_result_url("//duckduckgo.com/l/?rut=abc"))
        self.assertIsNone(resolve_result_url(""))

    def test_search_urls_carry_query_and_freshness(self):
        bing = bing_search_url('site:xiaohongshu.com "RLHF"', 7, 20)
        self.assertIn("bing.com/search?", bing)
        self.assertIn("site%3Axiaohongshu.com", bing)
        self.assertIn("ex1%3A%22ez2%22", bing)
        ddg = duckduckgo_search_url('site:xiaohongshu.com "RLHF"', 31)
        self.assertIn("html.duckduckgo.com/html/?", ddg)
        self.assertIn("df=m", ddg)
        self.assertNotIn("df=", duckduckgo_search_url("q", 400))


class ParserTests(unittest.TestCase):
    def test_parse_bing_results_extracts_all_titles(self):
        hits = parse_bing_results(BING_FIXTURE)
        self.assertEqual(len(hits), 5)
        self.assertEqual(hits[0]["title"], "RLHF 实战笔记：奖励模型到 PPO")
        self.assertIn("2501.12948", hits[0]["snippet"])

    def test_parse_duckduckgo_results_unwraps_redirects(self):
        hits = parse_duckduckgo_results(DDG_FIXTURE)
        self.assertEqual(len(hits), 2)
        self.assertTrue(hits[0]["url"].startswith("https://www.xiaohongshu.com/explore/67b1c2d3e4f60718293a4b5c"))
        self.assertEqual(hits[0]["title"], "DPO 与 GRPO 对比笔记")
        self.assertIn("2402.03300", hits[0]["snippet"])

    def test_challenge_page_parses_to_zero_hits(self):
        self.assertEqual(parse_duckduckgo_results(DDG_CHALLENGE_FIXTURE), [])
        self.assertEqual(parse_bing_results(""), [])


class FilterTests(unittest.TestCase):
    def test_collect_note_hits_keeps_only_clean_notes(self):
        hits = parse_bing_results(BING_FIXTURE)
        notes = collect_note_hits("RLHF", hits, CONFIG)
        self.assertEqual(len(notes), 1)
        note = notes[0]
        self.assertEqual(note["url"], "https://www.xiaohongshu.com/explore/66f1a2b3c4d5e6f708192a3b")
        self.assertEqual(note["keyword"], "RLHF")

    def test_promotional_detection(self):
        self.assertTrue(is_promotional("关注我，加微信领取资料包", CONFIG["exclude_terms"]))
        self.assertTrue(is_promotional("Comment +V for more", ["+v"]))
        self.assertFalse(is_promotional("GRPO 训练笔记与踩坑记录", CONFIG["exclude_terms"]))

    def test_extract_arxiv_ids(self):
        self.assertEqual(
            extract_arxiv_ids("对比 2501.12948v2 和 2402.03300，以及 2203.02155"),
            ["arxiv:2203.02155", "arxiv:2402.03300", "arxiv:2501.12948"],
        )
        self.assertEqual(extract_arxiv_ids("没有编号"), [])


class StoreTests(unittest.TestCase):
    EXISTING_TEXT = (
        "signals:\n"
        "  - id: community:handwritten-1\n"
        "    date: 2026-01-01\n"
        "    source: chinese-technical-blog\n"
        "    url: https://example.com/post\n"
        "    summary: A curated entry with a long single-line summary that must not be rewrapped by automated writes.\n"
        "    related_ids: [arxiv:2501.12948]\n"
    )

    def _new_signal(self, note_id: str, date: dt.date) -> dict:
        return {
            "id": f"community:xiaohongshu-{note_id}",
            "date": date,
            "source": "xiaohongshu",
            "url": f"https://www.xiaohongshu.com/explore/{note_id}",
            "summary": 'A Xiaohongshu note titled "GRPO 笔记" matched the technical keyword "GRPO".',
            "related_ids": ["arxiv:2501.12948"],
            "keyword": "GRPO",
        }

    def test_noop_run_leaves_file_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "community_signals.yaml"
            path.write_text(self.EXISTING_TEXT, encoding="utf-8")
            added = store_signals(path, [self._new_signal("66f1a2b3c4d5e6f708192a3b", dt.date(2026, 9, 15))], 200)
            self.assertEqual(added, 1)
            before = path.read_bytes()
            again = store_signals(path, [self._new_signal("66f1a2b3c4d5e6f708192a3b", dt.date(2026, 9, 16))], 200)
            self.assertEqual(again, 0)
            self.assertEqual(path.read_bytes(), before)

    def test_append_preserves_existing_bytes_and_style(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "community_signals.yaml"
            path.write_text(self.EXISTING_TEXT, encoding="utf-8")
            added = store_signals(path, [self._new_signal("66f1a2b3c4d5e6f708192a3b", dt.date(2026, 9, 15))], 200)
            self.assertEqual(added, 1)
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith(self.EXISTING_TEXT))
            self.assertIn("\n\n  - id: community:xiaohongshu-66f1a2b3c4d5e6f708192a3b\n", text)
            payload = yaml.safe_load(text)
            self.assertEqual(len(payload["signals"]), 2)
            self.assertEqual(payload["signals"][1]["source"], "xiaohongshu")

    def test_pruning_rewrites_only_over_cap(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "community_signals.yaml"
            path.write_text(self.EXISTING_TEXT, encoding="utf-8")
            new = [self._new_signal(f"66f1a2b3c4d5e6f708192a{i:02x}", dt.date(2026, 9, 15)) for i in range(3)]
            added = store_signals(path, new, max_stored=2)
            self.assertEqual(added, 3)
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
            self.assertEqual(len(payload["signals"]), 3)  # 1 curated + 2 newest xiaohongshu
            self.assertEqual(payload["signals"][0]["id"], "community:handwritten-1")

    def test_store_creates_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "community_signals.yaml"
            added = store_signals(path, [self._new_signal("66f1a2b3c4d5e6f708192a3b", dt.date(2026, 9, 15))], 200)
            self.assertEqual(added, 1)
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("signals:\n  - id:"))
            self.assertEqual(len(yaml.safe_load(text)["signals"]), 1)


class ScanTests(unittest.TestCase):
    def test_scan_end_to_end_with_mocked_backend(self):
        config = {
            **CONFIG,
            "query_template": 'site:xiaohongshu.com "{keyword}"',
            "request_delay_seconds": 0,
        }
        specs = [{"keyword": "RLHF", "direction": "preference-alignment"}]
        with patch("radar.xiaohongshu.fetch_html", return_value=BING_FIXTURE) as mocked_fetch:
            signals = scan(config, specs, ["bing", "duckduckgo"])
        self.assertEqual(mocked_fetch.call_count, 1)  # bing yielded notes; duckduckgo not queried
        self.assertEqual(len(signals), 1)
        signal = signals[0]
        self.assertEqual(signal["id"], "community:xiaohongshu-66f1a2b3c4d5e6f708192a3b")
        self.assertEqual(signal["related_ids"], ["arxiv:2402.03300", "arxiv:2501.12948"])
        self.assertEqual(signal["direction_hint"], "preference-alignment")

    def test_scan_falls_back_and_survives_backend_failure(self):
        config = {**CONFIG, "request_delay_seconds": 0}
        specs = [{"keyword": "GRPO"}]
        responses = [TimeoutError("timed out"), DDG_FIXTURE]
        with patch("radar.xiaohongshu.fetch_html", side_effect=responses):
            signals = scan(config, specs, ["bing", "duckduckgo"])
        self.assertEqual(len(signals), 1)
        self.assertEqual(signal_id_for(signals[0]["url"]), "community:xiaohongshu-67b1c2d3e4f60718293a4b5c")

    def test_scan_all_backends_dead_returns_empty(self):
        config = {**CONFIG, "request_delay_seconds": 0}
        with patch("radar.xiaohongshu.fetch_html", side_effect=OSError("blocked")):
            self.assertEqual(scan(config, [{"keyword": "RLHF"}], ["bing"]), [])


class SignalTests(unittest.TestCase):
    def test_signal_id_is_stable_and_note_based(self):
        url = "https://www.xiaohongshu.com/explore/66f1a2b3c4d5e6f708192a3b"
        self.assertEqual(signal_id_for(url), "community:xiaohongshu-66f1a2b3c4d5e6f708192a3b")
        self.assertEqual(signal_id_for(url), signal_id_for(url))

    def test_build_signal_schema_and_arxiv_linking(self):
        note = {
            "url": "https://www.xiaohongshu.com/explore/66f1a2b3c4d5e6f708192a3b",
            "title": "RLHF 实战笔记",
            "snippet": "参考 2501.12948 的 GRPO。",
            "keyword": "RLHF",
            "direction": "preference-alignment",
        }
        signal = build_signal(note, dt.date(2026, 9, 15))
        self.assertEqual(signal["source"], "xiaohongshu")
        self.assertEqual(signal["related_ids"], ["arxiv:2501.12948"])
        self.assertEqual(signal["direction_hint"], "preference-alignment")
        self.assertEqual(signal["date"], dt.date(2026, 9, 15))
        self.assertIn("RLHF", signal["summary"])

    def test_merge_signals_dedups_and_prunes_only_xiaohongshu(self):
        existing = [
            {"id": "community:other-1", "date": "2026-01-01", "source": "chinese-technical-blog"},
            {"id": "community:xiaohongshu-old", "date": "2026-01-02", "source": "xiaohongshu"},
        ]
        new = [
            {"id": "community:xiaohongshu-old", "date": "2026-09-15", "source": "xiaohongshu"},
            {"id": "community:xiaohongshu-mid", "date": "2026-06-01", "source": "xiaohongshu"},
            {"id": "community:xiaohongshu-new", "date": "2026-09-15", "source": "xiaohongshu"},
        ]
        merged, added = merge_signals(existing, new, max_stored=2)
        self.assertEqual(added, 2)
        ids = [signal["id"] for signal in merged]
        self.assertIn("community:other-1", ids)  # other sources are never pruned
        self.assertNotIn("community:xiaohongshu-old", ids)  # oldest xiaohongshu pruned
        self.assertEqual(len(merged), 3)

    def test_merge_signals_is_idempotent_on_rerun(self):
        existing = [{"id": "community:xiaohongshu-a", "date": "2026-09-01", "source": "xiaohongshu"}]
        rerun = [{"id": "community:xiaohongshu-a", "date": "2026-09-15", "source": "xiaohongshu"}]
        merged, added = merge_signals(existing, rerun, max_stored=200)
        self.assertEqual(added, 0)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["date"], "2026-09-01")  # original discovery date kept


if __name__ == "__main__":
    unittest.main()
