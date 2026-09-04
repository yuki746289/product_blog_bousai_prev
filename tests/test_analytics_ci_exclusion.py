import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AnalyticsCiExclusionTest(unittest.TestCase):
    def test_google_analytics_skips_ci_audit_requests(self):
        html = (ROOT / "templates" / "partials" / "google_analytics.html").read_text(encoding="utf-8")
        self.assertIn("params.get('ci_audit') === '1'", html)
        self.assertIn("window.__BOUSAI_ANALYTICS_DISABLED__ = true", html)
        self.assertIn("document.createElement('script')", html)
        self.assertIn("window.gtag('config', 'G-XQVLD5HMNG')", html)

        guard_pos = html.index("params.get('ci_audit') === '1'")
        loader_pos = html.index("document.createElement('script')")
        config_pos = html.index("window.gtag('config', 'G-XQVLD5HMNG')")
        self.assertLess(guard_pos, loader_pos)
        self.assertLess(guard_pos, config_pos)

    def test_lighthouse_urls_are_marked_as_ci_audits(self):
        workflow = (ROOT / ".github" / "workflows" / "performance-audit.yml").read_text(encoding="utf-8")
        expected = [
            "https://bousaikun.ashigaru.jp/?ci_audit=1",
            "https://bousaikun.ashigaru.jp/guide/first-disaster-preparedness.html?ci_audit=1",
            "https://bousaikun.ashigaru.jp/goods/portable-power-station-disaster.html?ci_audit=1",
        ]
        for url in expected:
            with self.subTest(url=url):
                self.assertIn(url, workflow)

        self.assertNotIn('"https://bousaikun.ashigaru.jp/"\n', workflow)
        self.assertNotIn('"https://bousaikun.ashigaru.jp/guide/first-disaster-preparedness.html"', workflow)
        self.assertNotIn('"https://bousaikun.ashigaru.jp/goods/portable-power-station-disaster.html"', workflow)


if __name__ == "__main__":
    unittest.main()
