# Created: 2026-09-02
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

    def test_common_assets_exist(self):
        self.assertTrue((PUBLIC / "bousai_common.css").exists())
        self.assertTrue((PUBLIC / "bousai_common.js").exists())
        self.assertTrue((PUBLIC / "assets" / "images" / "ai_b023_furniture_check_20260902.webp").exists())
        self.assertTrue((PUBLIC / "assets" / "images" / "ai_b024_outage_supplies_20260902.webp").exists())


if __name__ == "__main__":
    unittest.main()
