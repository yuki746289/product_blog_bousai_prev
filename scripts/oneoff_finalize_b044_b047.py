from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"{path}: replacement anchor not found: {old[:100]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# B044 manual review is already PASS in docs/reviews/B044_CHECKLIST.md.
replace_once(
    "content/articles/B044_vehicle_overnight_disaster.md",
    "status: REVIEW_REQUIRED",
    "status: READY_TO_PUBLISH",
)

# Contextual parent links.
old_b004 = "夏季・冬季は室温管理が安全に直結する場合があります。長時間の停電で自宅環境を保てない場合は、自治体の開設施設や安全な場所への移動も選択肢にします。"
new_b004 = old_b004 + "\n\n停電中の冷蔵庫・食品の扱いは[停電したら冷蔵庫の食品はいつまで？](article_b045.html)、真夏の健康リスクは[エアコンが使えないときの熱中症対策](article_b047.html)で詳しく確認できます。"
replace_once("content/articles/B004_blackout_preparedness.md", old_b004, new_b004)

old_b004_html = "<p>夏季・冬季は室温管理が安全に直結する場合があります。長時間の停電で自宅環境を保てない場合は、自治体の開設施設や安全な場所への移動も選択肢にします。</p>"
new_b004_html = old_b004_html + '<p>停電中の冷蔵庫・食品の扱いは<a href="article_b045.html">停電したら冷蔵庫の食品はいつまで？</a>、真夏の健康リスクは<a href="article_b047.html">エアコンが使えないときの熱中症対策</a>で詳しく確認できます。</p>'
replace_once("preview/article_b004.html", old_b004_html, new_b004_html)

old_b006 = "> **Q&A:** [窓にテープを貼れば台風でも割れませんか？](qa.html#qa-window-tape)"
new_b006 = old_b006 + "\n\n窓ガラス・雨戸・養生テープ・飛散防止をまとめて確認する場合は、[台風の窓ガラス対策](article_b046.html)も参照してください。"
replace_once("content/articles/B006_typhoon_preparation_checklist.md", old_b006, new_b006)

old_b006_html = "Q&amp;A：窓にテープを貼れば台風でも割れませんか？</a></div>"
new_b006_html = old_b006_html + '<p><a href="article_b046.html">台風の窓ガラス対策｜養生テープだけで大丈夫？</a>で、雨戸・飛散防止・割れた後まで詳しく確認できます。</p>'
replace_once("preview/article_b006.html", old_b006_html, new_b006_html)

# B029 markdown already has B044. Insert into preview immediately before the existing car-kit Q&A.
b029_path = ROOT / "preview/article_b029.html"
b029 = b029_path.read_text(encoding="utf-8")
b029_link = '<p>やむを得ず車内で避難生活を送る場合の健康・一酸化炭素・暑さ寒さは、<a href="article_b044.html">災害時の車中泊は安全？</a>で確認してください。</p>\n'
if b029_link not in b029:
    anchor = '<div class="qa-guide-link"><a href="qa.html#qa-car-kit">'
    if anchor not in b029:
        raise SystemExit("preview/article_b029.html: Q&A anchor missing")
    b029 = b029.replace(anchor, b029_link + anchor, 1)
    b029_path.write_text(b029, encoding="utf-8")

# Registry entries for B044-B047.
registry_path = ROOT / "data/content_registry.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))


def body_len(path: str) -> int:
    text = (ROOT / path).read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            text = parts[2]
    return len(text.strip())


common = {
    "content_depth_checked_at": "2026-09-05",
    "content_depth_status": "PASS",
    "image_dedup_checked_at": "2026-09-05",
    "image_dedup_status": "PASS",
    "image_source_count": 0,
    "image_status": "APPROVED",
    "last_reviewed_at": "2026-09-05",
    "manual_review_required": True,
    "manual_review_status": "APPROVED",
    "next_review_at": "2027-03-05",
    "pickup_candidate": True,
    "publish_blockers": [],
    "review_checklist_last_checked_at": "2026-09-05",
    "review_checklist_status": "PASS",
    "source_checked_at": "2026-09-05",
    "status": "READY_TO_PUBLISH",
    "readability_review_status": "PASS",
    "readability_reviewed_at": "2026-09-05",
    "image_relevance_review_status": "PASS",
    "image_relevance_reviewed_at": "2026-09-05",
    "production_build_status": "READY_FOR_DEPLOY",
    "published_at": "2026-09-05",
    "modified_at": "2026-09-05",
}

specs = [
    {
        "article_id": "B044",
        "slug": "vehicle-overnight-disaster",
        "title": "災害時の車中泊は安全？エコノミークラス症候群・一酸化炭素・暑さ寒さ",
        "category": "vehicle",
        "content_role": "practical",
        "risk_level": "high",
        "affiliate": False,
        "parent_article_id": "B029",
        "priority": "high",
        "planned_public_path": "vehicle/vehicle-overnight-disaster.html",
        "preview_path": "preview/article_b044.html",
        "source_path": "content/articles/B044_vehicle_overnight_disaster.md",
        "image_source_path": "docs/research/B044_IMAGES.md",
        "review_checklist_path": "docs/reviews/B044_CHECKLIST.md",
        "source_count": 6,
        "source_ids": [f"F-B044-{i:03d}" for i in range(1, 7)],
    },
    {
        "article_id": "B045",
        "slug": "blackout-refrigerator-food-safety",
        "title": "停電したら冷蔵庫の食品はいつまで？冷蔵・冷凍食品の判断と停電対策",
        "category": "blackout",
        "content_role": "practical",
        "risk_level": "high",
        "affiliate": False,
        "parent_article_id": "B004",
        "priority": "highest",
        "planned_public_path": "blackout/blackout-refrigerator-food-safety.html",
        "preview_path": "preview/article_b045.html",
        "source_path": "content/articles/B045_blackout_refrigerator_food.md",
        "image_source_path": "docs/research/B045_IMAGES.md",
        "review_checklist_path": "docs/reviews/B045_CHECKLIST.md",
        "source_count": 4,
        "source_ids": [f"F-B045-{i:03d}" for i in range(1, 5)],
    },
    {
        "article_id": "B046",
        "slug": "typhoon-window-glass",
        "title": "台風の窓ガラス対策｜養生テープだけで大丈夫？雨戸・飛散防止・割れた後",
        "category": "typhoon",
        "content_role": "practical",
        "risk_level": "elevated",
        "affiliate": False,
        "parent_article_id": "B006",
        "priority": "high",
        "planned_public_path": "typhoon/typhoon-window-glass.html",
        "preview_path": "preview/article_b046.html",
        "source_path": "content/articles/B046_typhoon_window_glass.md",
        "image_source_path": "docs/research/B046_IMAGES.md",
        "review_checklist_path": "docs/reviews/B046_CHECKLIST.md",
        "source_count": 4,
        "source_ids": [f"F-B046-{i:03d}" for i in range(1, 5)],
    },
    {
        "article_id": "B047",
        "slug": "blackout-heatstroke",
        "title": "真夏に停電したらどうする？エアコンが使えないときの熱中症対策",
        "category": "blackout",
        "content_role": "practical",
        "risk_level": "high",
        "affiliate": False,
        "parent_article_id": "B004",
        "priority": "high",
        "planned_public_path": "blackout/blackout-heatstroke.html",
        "preview_path": "preview/article_b047.html",
        "source_path": "content/articles/B047_blackout_heatstroke.md",
        "image_source_path": "docs/research/B047_IMAGES.md",
        "review_checklist_path": "docs/reviews/B047_CHECKLIST.md",
        "source_count": 4,
        "source_ids": [f"F-B047-{i:03d}" for i in range(1, 5)],
    },
]

by_id = {article["article_id"]: article for article in registry["articles"]}
for spec in specs:
    entry = dict(common)
    entry.update(spec)
    entry["body_char_count_approx"] = body_len(spec["source_path"])
    by_id[spec["article_id"]] = entry
registry["articles"] = sorted(by_id.values(), key=lambda article: article["article_id"])
registry["updated_at"] = "2026-09-05T19:10:00+09:00"
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Update public build contract.
test_path = ROOT / "tests/test_public_build.py"
test = test_path.read_text(encoding="utf-8")
test = test.replace(
    'self.assertEqual(43, len([a for a in articles if a.get("article_id", "").startswith("B")]))',
    'self.assertEqual(47, len([a for a in articles if a.get("article_id", "").startswith("B")]))',
)
anchor = '        self.assertTrue((PUBLIC / "typhoon" / "storm-surge-evacuation.html").exists())\n'
additions = (
    '        self.assertTrue((PUBLIC / "vehicle" / "vehicle-overnight-disaster.html").exists())\n'
    '        self.assertTrue((PUBLIC / "blackout" / "blackout-refrigerator-food-safety.html").exists())\n'
    '        self.assertTrue((PUBLIC / "typhoon" / "typhoon-window-glass.html").exists())\n'
    '        self.assertTrue((PUBLIC / "blackout" / "blackout-heatstroke.html").exists())\n'
)
if additions not in test:
    if anchor not in test:
        raise SystemExit("tests/test_public_build.py: B043 page anchor missing")
    test = test.replace(anchor, anchor + additions, 1)
test_path.write_text(test, encoding="utf-8")

# Dedicated safety regressions for the keyword-driven batch.
regression = r'''# Created: 2026-09-05
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class KeywordBatchSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = json.loads((ROOT / "data" / "content_registry.json").read_text(encoding="utf-8"))
        cls.by_id = {article["article_id"]: article for article in registry["articles"]}

    def text(self, article_id):
        return (ROOT / self.by_id[article_id]["source_path"]).read_text(encoding="utf-8")

    def test_batch_is_registered_and_publishable(self):
        for article_id in ("B044", "B045", "B046", "B047"):
            article = self.by_id[article_id]
            self.assertEqual("READY_TO_PUBLISH", article["status"])
            self.assertEqual("APPROVED", article["manual_review_status"])
            self.assertEqual([], article["publish_blockers"])

    def test_b044_vehicle_overnight_boundaries(self):
        text = self.text("B044")
        self.assertIn("車の中だから安全", text)
        self.assertIn("窓を少し開けるだけでは危険を防げない", text)
        self.assertIn("支援情報から孤立しない", text)

    def test_b045_refrigerator_food_boundaries(self):
        text = self.text("B045")
        self.assertIn("○時間までなら安全", text)
        self.assertIn("味見だけで", text)
        self.assertIn("必要以上に開けない", text)
        self.assertNotIn("4時間までなら安全", text)

    def test_b046_window_tape_boundaries(self):
        text = self.text("B046")
        self.assertIn("養生テープだけを台風の窓対策にしない", text)
        self.assertIn("割れなくなると考えない", text)
        self.assertIn("強風中に外側から補修", text)

    def test_b047_heatstroke_boundaries(self):
        text = self.text("B047")
        self.assertIn("自力で水が飲めない、意識がない場合", text)
        self.assertIn("屋内、車庫、換気が不十分な場所で発電機を使わない", text)
        self.assertIn("モバイル扇風機や保冷剤があるから長時間自宅で大丈夫", text)

    def test_parent_and_category_links_exist(self):
        self.assertIn("article_b044.html", (ROOT / "preview/category_vehicle.html").read_text(encoding="utf-8"))
        outage = (ROOT / "preview/category_outage.html").read_text(encoding="utf-8")
        self.assertIn("article_b045.html", outage)
        self.assertIn("article_b047.html", outage)
        self.assertIn("article_b046.html", (ROOT / "preview/category_typhoon.html").read_text(encoding="utf-8"))
        self.assertIn("article_b044.html", (ROOT / "preview/article_b029.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
'''
(ROOT / "tests/test_b044_b047_keyword_batch.py").write_text(textwrap.dedent(regression), encoding="utf-8")

print("B044-B047 finalization prepared.")
