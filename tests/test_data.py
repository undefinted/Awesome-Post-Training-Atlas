import unittest
from pathlib import Path

import yaml

from radar.site import analytics


ROOT = Path(__file__).resolve().parents[1]


class PaperDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.papers = yaml.safe_load((ROOT / "data" / "papers.yaml").read_text(encoding="utf-8"))["papers"]
        taxonomy = yaml.safe_load((ROOT / "config" / "taxonomy.yaml").read_text(encoding="utf-8"))
        cls.directions = {item["id"] for item in taxonomy["directions"]}
        labels = yaml.safe_load((ROOT / "config" / "labels.yaml").read_text(encoding="utf-8"))
        cls.labels = {item["id"] for item in labels["labels"]}
        methods = yaml.safe_load((ROOT / "config" / "method_families.yaml").read_text(encoding="utf-8"))
        cls.method_families = {item["id"]: item for item in methods["families"]}
        cls.method_axes = set(methods["axes"])

    def test_ids_are_unique(self):
        ids = [paper["id"].lower() for paper in self.papers]
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_fields_and_directions(self):
        required = {"id", "title", "date", "direction", "modalities", "tags", "key_idea", "url"}
        for paper in self.papers:
            self.assertFalse(required - set(paper), paper.get("id"))
            self.assertIn(paper["direction"], self.directions)
            self.assertTrue(str(paper["url"]).startswith("https://"))
            self.assertTrue(paper.get("authors"), paper["id"])
            self.assertFalse(set(paper.get("auto_labels", [])) - self.labels, paper["id"])
            if paper.get("institutions"):
                self.assertTrue(paper.get("institution_source"), paper["id"])
            if paper.get("venue"):
                self.assertTrue(paper.get("venue_source"), paper["id"])
                self.assertNotIn(paper["venue"].lower(), {"arxiv", "arxiv.org", "corr"})
            self.assertIn(paper.get("method_family"), self.method_families, paper["id"])
            self.assertIsInstance(paper.get("predecessors"), list, paper["id"])
            self.assertNotIn(paper["id"], paper.get("predecessors", []), paper["id"])
            self.assertFalse(set(paper.get("change_axes", [])) - self.method_axes, paper["id"])
            self.assertIsInstance(paper.get("transfer_ideas"), list, paper["id"])
            self.assertTrue(all(isinstance(idea, str) and idea.strip() for idea in paper.get("transfer_ideas", [])), paper["id"])

    def test_method_family_config(self):
        for family in self.method_families.values():
            self.assertTrue(family.get("title"), family.get("id"))
            self.assertTrue(family.get("description"), family.get("id"))
            self.assertTrue(family.get("color", "").startswith("#"), family.get("id"))
            self.assertTrue(family.get("transfer_ideas"), family.get("id"))

    def test_community_signal_schema(self):
        payload = yaml.safe_load((ROOT / "data" / "community_signals.yaml").read_text(encoding="utf-8"))
        required = {"id", "date", "source", "url", "summary", "related_ids"}
        for signal in payload["signals"]:
            self.assertFalse(required - set(signal), signal.get("id"))
            self.assertTrue(str(signal["url"]).startswith("https://"))

    def test_candidate_ids_are_unique(self):
        payload = yaml.safe_load((ROOT / "data" / "candidates.yaml").read_text(encoding="utf-8")) or {"papers": []}
        candidates = payload.get("papers", [])
        ids = [paper["id"].lower() for paper in candidates]
        self.assertEqual(len(ids), len(set(ids)))
        curated_ids = {paper["id"].lower() for paper in self.papers}
        self.assertFalse(curated_ids & set(ids))
        for paper in candidates:
            direction = paper.get("direction") or paper.get("suggested_direction")
            self.assertIn(direction, self.directions, paper["id"])
            self.assertIn("arxiv", " ".join(paper.get("source_signals", [])).lower(), paper["id"])
            self.assertTrue(paper.get("authors"), paper["id"])
            self.assertFalse(set(paper.get("auto_labels", [])) - self.labels, paper["id"])
            if paper.get("institutions"):
                self.assertTrue(paper.get("institution_source"), paper["id"])
            if paper.get("venue"):
                self.assertTrue(paper.get("venue_source"), paper["id"])
                self.assertNotIn(paper["venue"].lower(), {"arxiv", "arxiv.org", "corr"})

    def test_label_ids_are_unique(self):
        labels = yaml.safe_load((ROOT / "config" / "labels.yaml").read_text(encoding="utf-8"))["labels"]
        self.assertEqual(len(labels), len(self.labels))

    def test_direction_analytics_rows_are_chart_compatible(self):
        records = [
            {
                "id": "paper:1",
                "title": "Paper one",
                "date": "2025-01-01",
                "direction": "direction-a",
                "status": "curated",
                "url": "https://example.com/1",
                "methodFamily": None,
                "changeAxes": [],
                "transferIdeas": [],
                "predecessors": [],
            },
            {
                "id": "paper:2",
                "title": "Paper two",
                "date": "2025-02-01",
                "direction": "direction-b",
                "status": "discovery",
                "url": "https://example.com/2",
                "methodFamily": None,
                "changeAxes": [],
                "transferIdeas": [],
                "predecessors": [],
            },
        ]
        result = analytics(records, [{"id": "direction-a", "title": "A"}, {"id": "direction-b", "title": "B"}])
        self.assertEqual([row["count"] for row in result["directions"]], [1, 1])
        self.assertEqual([row["total"] for row in result["directions"]], [1, 1])


if __name__ == "__main__":
    unittest.main()
