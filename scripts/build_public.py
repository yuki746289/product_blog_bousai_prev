# Created: 2026-09-02
"""Build production static files from preview HTML.

- Uses data/content_registry.json planned_public_path for article URLs.
- Removes preview-only noindex/workflow labels.
- Injects Google Analytics.
- Rewrites internal links for production paths.
- Excludes contact.html while the contact channel is hidden.
"""

from __future__ import annotations

import json
import os
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "preview"
PUBLIC = ROOT / "public"
REGISTRY = ROOT / "data" / "content_registry.json"
GA_PARTIAL = ROOT / "templates" / "partials" / "google_analytics.html"
SITE_CONFIG = ROOT / "config" / "site.json"

STATIC_HTML_MAP = {
    "index.html": "index.html",
    "qa.html": "qa.html",
    "about.html": "about.html",
    "disclaimer.html": "disclaimer.html",
    "privacy.html": "privacy.html",
    "advertising.html": "advertising.html",
    # contact.html is intentionally not published while contact is hidden.
    "category_guide.html": "guide/index.html",
    "category_typhoon.html": "typhoon/index.html",
    "category_flood.html": "flood/index.html",
    "category_earthquake.html": "earthquake/index.html",
    "category_vehicle.html": "vehicle/index.html",
    "category_home.html": "home/index.html",
    "category_insurance.html": "insurance/index.html",
    "category_goods.html": "goods/index.html",
    "category_outage.html": "outage/index.html",
    "category_post_disaster.html": "post-disaster/index.html",
    "goods_water_food.html": "goods/water-food.html",
    "goods_toilet_hygiene.html": "goods/toilet-hygiene.html",
    "goods_light_information.html": "goods/light-information.html",
    "goods_power_charging.html": "goods/power-charging.html",
}

RESOURCE_TARGETS = {
    "bousai_common.css": "bousai_common.css",
    "bousai_common.js": "bousai_common.js",
}

WORKFLOW_LABEL_RE = re.compile(
    r"<span>\s*(?:記事ID:\s*B\d{3}|要目視確認|要レビュー|"
    r"REVIEW_REQUIRED|DRAFTED|READY_TO_PUBLISH)\s*</span>",
    re.IGNORECASE,
)
NOINDEX_RE = re.compile(
    r'<meta\s+name=["\']robots["\']\s+content=["\']noindex["\']\s*/?>',
    re.IGNORECASE,
)
ATTR_RE = re.compile(r'(?P<attr>href|src)=["\'](?P<url>[^"\']+)["\']', re.IGNORECASE)


def load_html_map() -> dict[str, str]:
    mapping = dict(STATIC_HTML_MAP)
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for article in registry["articles"]:
        preview_path = article.get("preview_path")
        public_path = article.get("planned_public_path")
        if preview_path and public_path:
            mapping[Path(preview_path).name] = public_path.lstrip("/")
    return mapping


def relative_target(current_output: str, target: str) -> str:
    parent = posixpath.dirname(current_output) or "."
    return posixpath.relpath(target, parent)


def rewrite_url(url: str, current_output: str, html_map: dict[str, str]) -> str:
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or url.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return url

    path = parts.path.replace("\\", "/")
    if not path:
        return url

    # Existing root-absolute production links are already suitable.
    if path.startswith("/"):
        return url

    normalized = path[2:] if path.startswith("./") else path
    target = None

    if normalized in html_map:
        target = html_map[normalized]
    elif posixpath.basename(normalized) in html_map and "/" not in normalized:
        target = html_map[posixpath.basename(normalized)]
    elif normalized in RESOURCE_TARGETS:
        target = RESOURCE_TARGETS[normalized]
    elif normalized.startswith("assets/"):
        target = normalized
    elif normalized.endswith(".html"):
        raise ValueError(f"Unknown internal HTML target: {url} from {current_output}")

    if target is None:
        return url

    rewritten = relative_target(current_output, target)
    return urlunsplit(("", "", rewritten, parts.query, parts.fragment))


def transform_html(source_name: str, output_path: str, html: str, html_map: dict[str, str], ga: str) -> str:
    html = NOINDEX_RE.sub("", html)
    html = WORKFLOW_LABEL_RE.sub("", html)

    def replace_attr(match: re.Match[str]) -> str:
        attr = match.group("attr")
        url = match.group("url")
        return f'{attr}="{rewrite_url(url, output_path, html_map)}"'

    html = ATTR_RE.sub(replace_attr, html)

    if "G-XQVLD5HMNG" not in html:
        if "</head>" not in html:
            raise ValueError(f"Missing </head>: {source_name}")
        html = html.replace("</head>", ga.rstrip() + "\n</head>", 1)

    return html


def write_search_engine_files(html_map: dict[str, str]) -> None:
    """Generate sitemap.xml and robots.txt from the production route map."""
    site_config = json.loads(SITE_CONFIG.read_text(encoding="utf-8"))
    base_url = site_config["public_base_url"].rstrip("/")

    urls: list[str] = []
    for output_path in sorted(set(html_map.values())):
        if output_path == "index.html":
            loc = base_url + "/"
        else:
            loc = f"{base_url}/{output_path}"
        urls.append(loc)

    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc in urls:
        sitemap_lines.extend([
            "  <url>",
            f"    <loc>{xml_escape(loc)}</loc>",
            "  </url>",
        ])
    sitemap_lines.append("</urlset>")
    (PUBLIC / "sitemap.xml").write_text("\n".join(sitemap_lines) + "\n", encoding="utf-8")

    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {base_url}/sitemap.xml\n"
    )
    (PUBLIC / "robots.txt").write_text(robots, encoding="utf-8")


def validate_public(html_map: dict[str, str]) -> None:
    html_files = sorted(PUBLIC.rglob("*.html"))
    if len(html_files) < 50:
        raise ValueError(f"Too few production HTML files: {len(html_files)}")

    errors: list[str] = []
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(PUBLIC).as_posix()

        if "noindex" in text.lower():
            errors.append(f"{rel}: noindex remains")
        if text.count("googletagmanager.com/gtag/js") != 1:
            errors.append(f"{rel}: GA script count != 1")
        if text.count("G-XQVLD5HMNG") < 2:
            errors.append(f"{rel}: GA measurement ID missing")
        if 'href="contact.html"' in text or "contact.html" in text:
            errors.append(f"{rel}: contact page link remains")
        if 'href="#"' in text:
            errors.append(f'{rel}: href="#" remains')
        if "準備中" in text:
            errors.append(f"{rel}: 準備中 remains")

        for match in ATTR_RE.finditer(text):
            url = match.group("url")
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or url.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                continue
            local_path = parts.path
            if not local_path:
                continue
            resolved = (path.parent / local_path).resolve()
            try:
                resolved.relative_to(PUBLIC.resolve())
            except ValueError:
                errors.append(f"{rel}: local target escapes public: {url}")
                continue
            if not resolved.exists():
                errors.append(f"{rel}: missing local target: {url}")

    if not (PUBLIC / "bousai_common.css").exists():
        errors.append("bousai_common.css missing")
    if not (PUBLIC / "bousai_common.js").exists():
        errors.append("bousai_common.js missing")
    if not (PUBLIC / "sitemap.xml").exists():
        errors.append("sitemap.xml missing")
    if not (PUBLIC / "robots.txt").exists():
        errors.append("robots.txt missing")

    if (PUBLIC / "sitemap.xml").exists():
        sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        if sitemap.count("<url>") != len(set(html_map.values())):
            errors.append("sitemap.xml URL count mismatch")
        if "contact.html" in sitemap:
            errors.append("sitemap.xml contains contact.html")

    if errors:
        raise ValueError("Public validation failed:\n" + "\n".join(errors))


def build() -> None:
    html_map = load_html_map()
    ga = GA_PARTIAL.read_text(encoding="utf-8")

    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)

    for source_name, output_path in sorted(html_map.items()):
        source = PREVIEW / source_name
        if not source.exists():
            raise FileNotFoundError(f"Missing preview source: {source}")
        if source_name == "contact.html":
            continue

        html = source.read_text(encoding="utf-8")
        transformed = transform_html(source_name, output_path, html, html_map, ga)
        destination = PUBLIC / output_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(transformed, encoding="utf-8")

    for resource in ("bousai_common.css", "bousai_common.js"):
        shutil.copy2(PREVIEW / resource, PUBLIC / resource)

    src_assets = PREVIEW / "assets"
    if src_assets.exists():
        shutil.copytree(src_assets, PUBLIC / "assets")

    write_search_engine_files(html_map)
    validate_public(html_map)


if __name__ == "__main__":
    build()
