# Created: 2026-09-02
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

    def test_common_assets_exist(self):
        self.assertTrue((PUBLIC / "bousai_common.css").exists())
        self.assertTrue((PUBLIC / "bousai_common.js").exists())
        self.assertTrue((PUBLIC / "assets" / "images" / "ai_b023_furniture_check_20260902.webp").exists())
        self.assertTrue((PUBLIC / "assets" / "images" / "ai_b024_outage_supplies_20260902.webp").exists())

    def test_sitemap_and_robots_exist_and_cover_public_html(self):
        sitemap_path = PUBLIC / "sitemap.xml"
        robots_path = PUBLIC / "robots.txt"
        self.assertTrue(sitemap_path.exists())
        self.assertTrue(robots_path.exists())

        sitemap = sitemap_path.read_text(encoding="utf-8")
        robots = robots_path.read_text(encoding="utf-8")
        self.assertEqual(50, sitemap.count("<url>"))
        self.assertIn("https://bousaikun.ashigaru.jp/", sitemap)
        self.assertIn("https://bousaikun.ashigaru.jp/goods/portable-power-station-disaster.html", sitemap)
        self.assertNotIn("contact.html", sitemap)
        self.assertIn("User-agent: *", robots)
        self.assertIn("Allow: /", robots)
        self.assertIn("Sitemap: https://bousaikun.ashigaru.jp/sitemap.xml", robots)


if __name__ == "__main__":
    unittest.main()
