# Created: 2026-09-03
"""Localize redistributable Wikimedia Commons article images for production.

This script runs after scripts/build_public.py. It only rewrites images inside
article figure blocks that explicitly attribute Wikimedia Commons. Product and
manufacturer images are intentionally excluded.

Behavior:
- downloads allow-listed Commons image URLs;
- follows only Commons -> upload.wikimedia.org redirects;
- converts to WebP and caps width at 1280 px;
- writes stable hashed assets under public/assets/images/commons/;
- adds intrinsic width/height to reduce layout shift;
- gives eager feature images high fetch priority;
- preserves the visible attribution and adds a Commons source-page link when
  the caption did not already contain one;
- leaves the original external URL unchanged if an individual download fails.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import posixpath
import re
import time
from pathlib import Path
from urllib.parse import quote, unquote, urlparse
from urllib.request import Request, urlopen

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ASSET_DIR = PUBLIC / "assets" / "images" / "commons"
MANIFEST = ASSET_DIR / "manifest.json"

ALLOWED_SOURCE_HOSTS = {"commons.wikimedia.org", "upload.wikimedia.org"}
ALLOWED_FINAL_HOSTS = {"commons.wikimedia.org", "upload.wikimedia.org"}
FIGURE_RE = re.compile(
    r"(?P<open><figure\\b(?P<attrs>[^>]*)>)(?P<body>.*?)(?P<close></figure>)",
    re.IGNORECASE | re.DOTALL,
)
IMG_RE = re.compile(r"<img\\b[^>]*>", re.IGNORECASE | re.DOTALL)
SRC_RE = re.compile(r'\\bsrc=(?P<q>["\\\'])(?P<src>.*?)(?P=q)', re.IGNORECASE | re.DOTALL)
FIGCAPTION_RE = re.compile(
    r"(?P<open><figcaption\\b[^>]*>)(?P<body>.*?)(?P<close></figcaption>)",
    re.IGNORECASE | re.DOTALL,
)


def is_eligible_figure(attrs: str, body: str) -> bool:
    class_match = re.search(r'class=["\\\']([^"\\\']+)["\\\']', attrs, re.IGNORECASE)
    classes = set(class_match.group(1).split()) if class_match else set()
    if not ({"article-feature-image", "article-inline-image"} & classes):
        return False
    if "Wikimedia Commons" not in body:
        return False
    img_match = IMG_RE.search(body)
    if not img_match:
        return False
    src_match = SRC_RE.search(img_match.group(0))
    if not src_match:
        return False
    host = (urlparse(html.unescape(src_match.group("src"))).hostname or "").lower()
    return host in ALLOWED_SOURCE_HOSTS


def commons_description_url(source_url: str) -> str | None:
    parsed = urlparse(html.unescape(source_url))
    path = unquote(parsed.path)

    marker = "/wiki/Special:Redirect/file/"
    if marker in path:
        filename = path.split(marker, 1)[1]
        return "https://commons.wikimedia.org/wiki/File:" + quote(filename, safe="()_,-.%")

    if parsed.hostname == "upload.wikimedia.org":
        parts = [part for part in path.split("/") if part]
        if len(parts) >= 2:
            candidate = parts[-2] if "/thumb/" in path else parts[-1]
            return "https://commons.wikimedia.org/wiki/File:" + quote(candidate, safe="()_,-.%")
    return None


def stable_asset_name(source_url: str) -> str:
    digest = hashlib.sha256(html.unescape(source_url).encode("utf-8")).hexdigest()[:16]
    return f"commons_{digest}.webp"


def download_image(source_url: str, retries: int = 3) -> tuple[bytes, str]:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            request = Request(
                html.unescape(source_url),
                headers={
                    "User-Agent": (
                        "bousai-kurashi-guide-image-localizer/1.0 "
                        "(+https://bousaikun.ashigaru.jp/)"
                    )
                },
            )
            with urlopen(request, timeout=40) as response:
                final_url = response.geturl()
                host = (urlparse(final_url).hostname or "").lower()
                if host not in ALLOWED_FINAL_HOSTS:
                    raise ValueError(f"unexpected redirect host: {host}")
                return response.read(), final_url
        except Exception as exc:  # network failures should not block the whole deploy
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(1.5 * (attempt + 1))
    assert last_error is not None
    raise last_error


def optimize_webp(data: bytes, destination: Path) -> tuple[int, int, int]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(io.BytesIO(data)) as original:
        image = ImageOps.exif_transpose(original)
        if image.width > 1280:
            height = round(image.height * 1280 / image.width)
            image = image.resize((1280, height), Image.Resampling.LANCZOS)

        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA" if "transparency" in image.info else "RGB")

        image.save(destination, format="WEBP", quality=82, method=6)
        return image.width, image.height, destination.stat().st_size


def add_image_attributes(tag: str, width: int, height: int, feature: bool) -> str:
    if not re.search(r"\\bwidth=", tag, re.IGNORECASE):
        tag = tag[:-1] + f' width="{width}">'
    if not re.search(r"\\bheight=", tag, re.IGNORECASE):
        tag = tag[:-1] + f' height="{height}">'
    if not re.search(r"\\bdecoding=", tag, re.IGNORECASE):
        tag = tag[:-1] + ' decoding="async">'
    if feature and 'loading="eager"' in tag and not re.search(r"\\bfetchpriority=", tag, re.IGNORECASE):
        tag = tag[:-1] + ' fetchpriority="high">'
    return tag


def ensure_source_link(body: str, source_url: str) -> str:
    caption_match = FIGCAPTION_RE.search(body)
    if not caption_match:
        return body
    if re.search(r'href=["\\\']https://commons\\.wikimedia\\.org/', caption_match.group(0), re.IGNORECASE):
        return body

    description_url = commons_description_url(source_url)
    if not description_url:
        return body

    appendix = (
        ' <a href="' + description_url + '" target="_blank" '
        'rel="noopener noreferrer">Wikimedia Commonsの元画像</a>'
    )
    replacement = (
        caption_match.group("open")
        + caption_match.group("body").rstrip()
        + appendix
        + caption_match.group("close")
    )
    return body[: caption_match.start()] + replacement + body[caption_match.end() :]


def localize_html_file(path: Path, cache: dict[str, dict]) -> tuple[int, int]:
    original_html = path.read_text(encoding="utf-8")
    localized_count = 0
    failed_count = 0

    def replace_figure(match: re.Match[str]) -> str:
        nonlocal localized_count, failed_count
        attrs = match.group("attrs")
        body = match.group("body")
        if not is_eligible_figure(attrs, body):
            return match.group(0)

        img_match = IMG_RE.search(body)
        assert img_match is not None
        tag = img_match.group(0)
        src_match = SRC_RE.search(tag)
        assert src_match is not None
        source_url = src_match.group("src")

        entry = cache.get(source_url)
        if entry is None:
            asset_name = stable_asset_name(source_url)
            destination = ASSET_DIR / asset_name
            try:
                raw, final_url = download_image(source_url)
                width, height, optimized_bytes = optimize_webp(raw, destination)
                entry = {
                    "source_url": html.unescape(source_url),
                    "final_url": final_url,
                    "local_path": f"assets/images/commons/{asset_name}",
                    "width": width,
                    "height": height,
                    "source_bytes": len(raw),
                    "optimized_bytes": optimized_bytes,
                    "status": "localized",
                }
            except Exception as exc:
                entry = {
                    "source_url": html.unescape(source_url),
                    "status": "failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            cache[source_url] = entry

        if entry["status"] != "localized":
            failed_count += 1
            return match.group(0)

        page_rel = path.relative_to(PUBLIC).as_posix()
        local_url = posixpath.relpath(entry["local_path"], posixpath.dirname(page_rel) or ".")
        new_tag = SRC_RE.sub(
            lambda m: f'src="{local_url}"',
            tag,
            count=1,
        )
        feature = "article-feature-image" in attrs
        new_tag = add_image_attributes(new_tag, entry["width"], entry["height"], feature)
        new_body = body[: img_match.start()] + new_tag + body[img_match.end() :]
        new_body = ensure_source_link(new_body, source_url)
        localized_count += 1
        return match.group("open") + new_body + match.group("close")

    rewritten = FIGURE_RE.sub(replace_figure, original_html)
    if rewritten != original_html:
        path.write_text(rewritten, encoding="utf-8")
    return localized_count, failed_count


def run(min_localized: int = 0) -> dict:
    if not PUBLIC.exists():
        raise FileNotFoundError("public directory does not exist; run build_public.py first")

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    cache: dict[str, dict] = {}
    page_results: list[dict] = []
    total_localized = 0
    total_failed = 0

    for page in sorted(PUBLIC.rglob("*.html")):
        localized, failed = localize_html_file(page, cache)
        if localized or failed:
            page_results.append(
                {
                    "page": page.relative_to(PUBLIC).as_posix(),
                    "localized": localized,
                    "failed": failed,
                }
            )
        total_localized += localized
        total_failed += failed

    assets = sorted(cache.values(), key=lambda item: item["source_url"])
    unique_localized = sum(1 for item in assets if item["status"] == "localized")
    unique_failed = sum(1 for item in assets if item["status"] == "failed")
    source_bytes = sum(item.get("source_bytes", 0) for item in assets)
    optimized_bytes = sum(item.get("optimized_bytes", 0) for item in assets)

    manifest = {
        "generated_by": "scripts/localize_commons_images.py",
        "pages_with_eligible_images": len(page_results),
        "image_occurrences_localized": total_localized,
        "image_occurrences_failed": total_failed,
        "unique_images_localized": unique_localized,
        "unique_images_failed": unique_failed,
        "source_bytes": source_bytes,
        "optimized_bytes": optimized_bytes,
        "saved_bytes": max(0, source_bytes - optimized_bytes),
        "pages": page_results,
        "assets": assets,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({k: v for k, v in manifest.items() if k not in {"pages", "assets"}}, ensure_ascii=False))
    if total_localized < min_localized:
        raise SystemExit(
            f"localized image occurrences {total_localized} < required minimum {min_localized}"
        )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-localized", type=int, default=0)
    args = parser.parse_args()
    run(min_localized=args.min_localized)


if __name__ == "__main__":
    main()
