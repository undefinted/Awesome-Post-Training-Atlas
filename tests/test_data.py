import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


class PaperDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.papers = yaml.safe_load((ROOT / "data" / "papers.yaml").read_text(encoding="utf-8"))["papers"]
        taxonomy = yaml.safe_load((ROOT / "config" / "taxonomy.yaml").read_text(encoding="utf-8"))
        cls.directions = {item["id"] for item in taxonomy["directions"]}

    def test_ids_are_unique(self):
        ids = [paper["id"].lower() for paper in self.papers]
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_fields_and_directions(self):
        required = {"id", "title", "date", "direction", "modalities", "tags", "key_idea", "url"}
        for paper in self.papers:
            self.assertFalse(required - set(paper), paper.get("id"))
            self.assertIn(paper["direction"], self.directions)
            self.assertTrue(str(paper["url"]).startswith("https://"))


if __name__ == "__main__":
    unittest.main()

