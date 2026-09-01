# Created: 2026-09-01 09:00 JST

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT_ID = "G-XQVLD5HMNG"


class AnalyticsConfigurationTests(unittest.TestCase):
    def test_site_config_has_expected_measurement_id(self):
        config = json.loads((ROOT / "config" / "site.json").read_text(encoding="utf-8"))
        analytics = config["analytics"]
        self.assertTrue(analytics["enabled"])
        self.assertTrue(analytics["required_on_all_public_pages"])
        self.assertEqual(MEASUREMENT_ID, analytics["measurement_id"])

    def test_google_analytics_partial_contains_measurement_id_once_per_call(self):
        html = (ROOT / "templates" / "partials" / "google_analytics.html").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            f"https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}",
            html,
        )
        self.assertIn(f"gtag('config', '{MEASUREMENT_ID}');", html)
        self.assertEqual(1, html.count("googletagmanager.com/gtag/js"))


if __name__ == "__main__":
    unittest.main()
