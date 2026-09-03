# Created: 2026-09-02
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


class PublicBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_public.py")], cwd=ROOT, check=True)

    def test_expected_public_pages_exist(self):
        self.assertTrue((PUBLIC / "index.html").exists())
        self.assertTrue((PUBLIC / "qa.html").exists())
        self.assertTrue((PUBLIC / "guide" / "first-disaster-preparedness.html").exists())
        self.assertTrue((PUBLIC / "vehicle" / "car-flood-submersion.html").exists())
        self.assertTrue((PUBLIC / "goods" / "portable-power-station-disaster.html").exists())
        self.assertTrue((PUBLIC / "goods" / "water-food.html").exists())

    def test_contact_is_not_published(self):
        self.assertFalse((PUBLIC / "contact.html").exists())

    def test_all_html_has_ga_and_no_noindex(self):
        html_files = list(PUBLIC.rglob("*.html"))
        self.assertGreaterEqual(len(html_files), 50)
        for path in html_files:
            html = path.read_text(encoding="utf-8")
            self.assertEqual(1, html.count("googletagmanager.com/gtag/js"), path)
            self.assertNotIn("noindex", html.lower(), path)
            self.assertNotIn('href="#"', html, path)
            self.assertNotIn("準備中", html, path)

    def test_all_html_has_unique_title_and_description(self):
        titles = {}
        descriptions = {}
        html_files = sorted(PUBLIC.rglob("*.html"))

        for path in html_files:
            html = path.read_text(encoding="utf-8")
            title_match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
            self.assertIsNotNone(title_match, path)
            title = " ".join(title_match.group(1).split())
            self.assertTrue(title, path)
            self.assertNotIn(title, titles, f"{path} duplicates {titles.get(title)}")
            titles[title] = path

            description_match = re.search(
                r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']',
                html,
                flags=re.IGNORECASE,
            )
            self.assertIsNotNone(description_match, path)
            description = " ".join(description_match.group(1).split())
            self.assertTrue(description, path)
            self.assertNotIn(
                description,
                descriptions,
                f"{path} duplicates {descriptions.get(description)}",
            )
            descriptions[description] = path


    def test_article_dates_and_structured_data(self):
        registry = json.loads((ROOT / "data" / "content_registry.json").read_text(encoding="utf-8"))
        articles = registry["articles"]
        self.assertEqual(35, len([a for a in articles if a.get("article_id", "").startswith("B")]))

        for article in articles:
            output = PUBLIC / article["planned_public_path"]
            html = output.read_text(encoding="utf-8")

            published = article["published_at"]
            modified = article["modified_at"]
            checked = article["source_checked_at"]
            self.assertIn(f'公開日: <time datetime="{published}">', html, output)
            self.assertIn(f'最終更新日: <time datetime="{modified}">', html, output)
            self.assertIn(f'情報確認日: <time datetime="{checked}">', html, output)

            marker = '<script type="application/ld+json" data-generated="article-structured-data">'
            self.assertEqual(1, html.count(marker), output)
            json_start = html.index(marker) + len(marker)
            json_end = html.index("</script>", json_start)
            payload = json.loads(html[json_start:json_end])
            graph = payload["@graph"]
            posting = next(node for node in graph if node["@type"] == "BlogPosting")
            breadcrumb = next(node for node in graph if node["@type"] == "BreadcrumbList")
            self.assertEqual(article["title"], posting["headline"], output)
            self.assertEqual(published, posting["datePublished"], output)
            self.assertEqual(modified, posting["dateModified"], output)
            self.assertEqual(3, len(breadcrumb["itemListElement"]), output)
            self.assertEqual(article["title"], breadcrumb["itemListElement"][-1]["name"], output)


    def test_practical_articles_have_saveable_action_check(self):
        registry = json.loads((ROOT / "data" / "content_registry.json").read_text(encoding="utf-8"))
        practical = [a for a in registry["articles"] if a.get("content_role") == "practical"]
        self.assertGreater(len(practical), 0)

        for article in practical:
            output = PUBLIC / article["planned_public_path"]
            html = output.read_text(encoding="utf-8")
            headings = " ".join(re.findall(r"<h2>(.*?)</h2>", html, flags=re.IGNORECASE | re.DOTALL))
            headings = re.sub(r"<[^>]+>", "", headings)
            self.assertRegex(headings, r"チェック|項目|行動", output)
            self.assertTrue(
                'class="checklist"' in html or "<table>" in html or "<ol>" in html,
                output,
            )


    def test_key_product_guides_have_conditional_calculation_examples(self):
        pages = [
            PUBLIC / "goods" / "water-food.html",
            PUBLIC / "goods" / "toilet-hygiene.html",
            PUBLIC / "goods" / "power-charging.html",
        ]
        for page in pages:
            html = page.read_text(encoding="utf-8")
            self.assertIn("概算例：", html, page)
            self.assertRegex(html, r"仮定|目安|個人差|調整", page)

    def test_listing_commons_images_request_reduced_width(self):
        pages = [PUBLIC / "index.html", *sorted(PUBLIC.glob("*/index.html"))]
        for page in pages:
            if not page.exists():
                continue
            html = page.read_text(encoding="utf-8")
            self.assertNotRegex(html, r'commons\.wikimedia\.org/[^"\']+\?width=(?:960|1280)', page)
            self.assertNotRegex(html, r'upload\.wikimedia\.org/[^"\']+/960px-', page)


    def test_source_boxes_do_not_display_raw_urls(self):
        raw_url_text = re.compile(r">\s*https?://[^<]+</a>", re.IGNORECASE)
        for page in sorted(PUBLIC.rglob("*.html")):
            html = page.read_text(encoding="utf-8")
            source_boxes = re.findall(
                r'<section\s+class=["\']source-box["\'][^>]*>(.*?)</section>',
                html,
                flags=re.IGNORECASE | re.DOTALL,
            )
            for source_box in source_boxes:
                self.assertIsNone(raw_url_text.search(source_box), page)


    def test_category_pages_do_not_render_literal_newline_tokens(self):
        for page in sorted(PUBLIC.glob("*/index.html")):
            html = page.read_text(encoding="utf-8")
            self.assertNotIn(r"</a>\n<a", html, page)
        for page in sorted(PUBLIC.glob("category_*.html")):
            html = page.read_text(encoding="utf-8")
            self.assertNotIn(r"</a>\n<a", html, page)

    def test_common_assets_exist(self):
        self.assertTrue((PUBLIC / "bousai_common.css").exists())
        self.assertTrue((PUBLIC / "bousai_common.js").exists())
        self.assertTrue((PUBLIC / "bousai_home.css").exists())
        self.assertTrue((PUBLIC / "bousai_home.js").exists())
        self.assertTrue((PUBLIC / "assets" / "images" / "ai_b023_furniture_check_20260902.webp").exists())
        self.assertTrue((PUBLIC / "assets" / "images" / "ai_b024_outage_supplies_20260902.webp").exists())

    def test_homepage_uses_home_specific_assets(self):
        home = (PUBLIC / "index.html").read_text(encoding="utf-8")
        article = (PUBLIC / "guide" / "first-disaster-preparedness.html").read_text(encoding="utf-8")
        common_js = (PUBLIC / "bousai_common.js").read_text(encoding="utf-8")
        home_js = (PUBLIC / "bousai_home.js").read_text(encoding="utf-8")
        common_css = (PUBLIC / "bousai_common.css").read_text(encoding="utf-8")
        home_css = (PUBLIC / "bousai_home.css").read_text(encoding="utf-8")

        self.assertIn('href="bousai_home.css"', home)
        self.assertIn('src="bousai_home.js"', home)
        self.assertNotIn("bousai_home.css", article)
        self.assertNotIn("bousai_home.js", article)
        self.assertNotIn("initRealtimePanel", common_js)
        self.assertIn("initRealtimePanel", home_js)
        self.assertNotIn(".realtime-section", common_css)
        self.assertIn(".realtime-section", home_css)

    def test_realtime_panel_avoids_scheduler_ui_copy(self):
        home = (PUBLIC / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("自動更新", home)
        self.assertNotIn("約10分間隔", home)
        self.assertIn("data-realtime-updated", home)
        self.assertIn('class="realtime-item"', home)

    def test_sitemap_and_robots_exist_and_cover_public_html(self):
        sitemap_path = PUBLIC / "sitemap.xml"
        robots_path = PUBLIC / "robots.txt"
        self.assertTrue(sitemap_path.exists())
        self.assertTrue(robots_path.exists())

        sitemap = sitemap_path.read_text(encoding="utf-8")
        robots = robots_path.read_text(encoding="utf-8")
        self.assertEqual(len(list(PUBLIC.rglob("*.html"))), sitemap.count("<url>"))
        self.assertIn("https://bousaikun.ashigaru.jp/", sitemap)
        self.assertIn("https://bousaikun.ashigaru.jp/goods/portable-power-station-disaster.html", sitemap)
        self.assertIn("https://bousaikun.ashigaru.jp/guide/emergency-food-expiration.html", sitemap)
        self.assertIn("https://bousaikun.ashigaru.jp/guide/emergency-bag-capacity.html", sitemap)
        self.assertNotIn("contact.html", sitemap)
        self.assertIn("User-agent: *", robots)
        self.assertIn("Allow: /", robots)
        self.assertIn("Sitemap: https://bousaikun.ashigaru.jp/sitemap.xml", robots)


if __name__ == "__main__":
    unittest.main()
