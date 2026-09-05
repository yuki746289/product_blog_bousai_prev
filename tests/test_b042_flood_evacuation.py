# Created: 2026-09-05
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class B042FloodEvacuationTests(unittest.TestCase):
    def test_b042_is_high_risk_reviewed_and_registered(self):
        registry = json.loads((ROOT / "data" / "content_registry.json").read_text(encoding="utf-8"))
        article = next(a for a in registry["articles"] if a.get("article_id") == "B042")
        self.assertEqual("high", article["risk_level"])
        self.assertTrue(article["manual_review_required"])
        self.assertEqual("APPROVED", article["manual_review_status"])
        self.assertEqual("PASS", article["review_checklist_status"])
        self.assertEqual("flood/flood-river-evacuation.html", article["planned_public_path"])

    def test_b042_keeps_core_safety_boundaries(self):
        article = (ROOT / "content" / "articles" / "B042_flood_river_evacuation.md").read_text(encoding="utf-8")
        required = [
            "警戒レベル4までに危険な場所から避難",
            "黒・レベル5を避難開始の合図にしない",
            "大河川の外水氾濫を洪水キキクルだけで判断",
            "川の水位を見に行かない",
            "屋内安全確保",
            "夜間・暴風になる前",
        ]
        for phrase in required:
            self.assertIn(phrase, article)
        self.assertNotIn("2階なら安全", article.split("当サイトだけで", 1)[-1])
        self.assertNotIn("川から1km", article)

    def test_b042_has_evidence_and_preview(self):
        for path in [
            ROOT / "docs" / "research" / "B042_FLOOD_EVACUATION_BRIEF.md",
            ROOT / "docs" / "research" / "B042_SOURCES.md",
            ROOT / "docs" / "research" / "B042_IMAGES.md",
            ROOT / "docs" / "reviews" / "B042_CHECKLIST.md",
            ROOT / "preview" / "article_b042.html",
        ]:
            self.assertTrue(path.exists(), path)


if __name__ == "__main__":
    unittest.main()
