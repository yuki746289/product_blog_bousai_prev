# Created: 2026-09-03
"""Build compact homepage disaster information from JMA PULL XML feeds."""
from __future__ import annotations

import argparse
import json
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Iterable

JST = timezone(timedelta(hours=9))
JMA_PULL_PAGE = "https://xml.kishou.go.jp/xmlpull.html"
JMA_QUAKE_PAGE = "https://www.jma.go.jp/bosai/map.html#contents=earthquake_map"
JMA_WARNING_PAGE = "https://www.jma.go.jp/bosai/map.html#contents=warning"
JMA_TYPHOON_PAGE = "https://www.jma.go.jp/bosai/map.html#contents=typhoon"
FEEDS = {
    "extra_high": "https://www.data.jma.go.jp/developer/xml/feed/extra.xml",
    "eqvol_high": "https://www.data.jma.go.jp/developer/xml/feed/eqvol.xml",
    "extra_long": "https://www.data.jma.go.jp/developer/xml/feed/extra_l.xml",
    "eqvol_long": "https://www.data.jma.go.jp/developer/xml/feed/eqvol_l.xml",
}
USER_AGENT = "bousai-kurashi-guide-realtime/1.0 (+https://bousaikun.ashigaru.jp/)"
WARNING_TITLES = ("気象特別警報・警報・注意報", "気象警報・注意報")
QUAKE_TITLES = ("震源・震度情報", "震度速報", "震源に関する情報")
TYPHOON_TITLE_WORDS = ("台風", "熱帯低気圧")
END_TYPHOON_WORDS = ("熱帯低気圧に変わ", "温帯低気圧に変わ", "消滅")
INTENSITY_ORDER = {
    "1": 1, "2": 2, "3": 3, "4": 4, "5-": 5, "5弱": 5,
    "5+": 6, "5強": 6, "6-": 7, "6弱": 7, "6+": 8, "6強": 8, "7": 9,
}
INTENSITY_LABEL = {"5-": "5弱", "5+": "5強", "6-": "6弱", "6+": "6強"}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def direct_child_text(node: ET.Element | None, name: str) -> str | None:
    if node is None:
        return None
    for item in list(node):
        if local_name(item.tag) == name and item.text and item.text.strip():
            return item.text.strip()
    return None


def first_text(node: ET.Element | None, name: str) -> str | None:
    if node is None:
        return None
    for item in node.iter():
        if local_name(item.tag) == name and item.text and item.text.strip():
            return item.text.strip()
    return None


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def fetch_bytes(url: str, retries: int = 3, timeout: int = 25) -> bytes:
    last_error = None
    for attempt in range(retries):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except Exception as exc:
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(attempt + 1)
    raise last_error


def parse_atom(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    entries = []
    for entry in root.iter():
        if local_name(entry.tag) != "entry":
            continue
        link = ""
        for child in list(entry):
            if local_name(child.tag) == "link" and child.attrib.get("href"):
                link = child.attrib["href"]
                break
        if link:
            entries.append({
                "title": direct_child_text(entry, "title") or "",
                "updated": direct_child_text(entry, "updated"),
                "id": direct_child_text(entry, "id") or "",
                "link": link,
            })
    return sorted(entries, key=lambda item: item.get("updated") or "")


def common_head(root: ET.Element) -> dict:
    head = next((item for item in root.iter() if local_name(item.tag) == "Head"), None)
    if head is None:
        return {}
    headline = next((item for item in head.iter() if local_name(item.tag) == "Headline"), None)
    return {
        "title": direct_child_text(head, "Title"),
        "report_time": direct_child_text(head, "ReportDateTime"),
        "target_time": direct_child_text(head, "TargetDateTime"),
        "event_id": direct_child_text(head, "EventID"),
        "headline": direct_child_text(headline, "Text"),
    }


def intensity_max(values: Iterable[str]) -> str | None:
    best, rank = None, -1
    for raw in values:
        value = raw.strip()
        value_rank = INTENSITY_ORDER.get(value, -1)
        if value_rank > rank:
            best, rank = INTENSITY_LABEL.get(value, value), value_rank
    return best


def parse_earthquake(xml_bytes: bytes, source_xml: str = "") -> dict:
    root = ET.fromstring(xml_bytes)
    head = common_head(root)
    hypocenter = None
    for node in root.iter():
        if local_name(node.tag) == "Hypocenter":
            area = next((x for x in node.iter() if local_name(x.tag) == "Area"), None)
            hypocenter = first_text(area, "Name")
            break
    magnitude = next(
        (node.text.strip() for node in root.iter()
         if local_name(node.tag) == "Magnitude" and node.text and node.text.strip()),
        None,
    )
    max_int = intensity_max(
        node.text for node in root.iter()
        if local_name(node.tag) == "MaxInt" and node.text
    )
    return {
        "event_id": head.get("event_id"),
        "title": head.get("title") or "地震情報",
        "time": head.get("target_time") or head.get("report_time"),
        "area": hypocenter,
        "magnitude": magnitude,
        "max_intensity": max_int,
        "headline": head.get("headline"),
        "official_url": JMA_QUAKE_PAGE,
        "source_xml": source_xml,
    }


def warning_information_nodes(root: ET.Element) -> list[ET.Element]:
    preferred, fallback = [], []
    for node in root.iter():
        if local_name(node.tag) != "Information":
            continue
        info_type = node.attrib.get("type", "")
        if "警報" not in info_type:
            continue
        fallback.append(node)
        if "府県予報区" in info_type:
            preferred.append(node)
    return preferred or fallback


def parse_warning_updates(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    head = common_head(root)
    report_time = head.get("report_time") or head.get("target_time")
    updates = []
    for info in warning_information_nodes(root):
        for item in list(info):
            if local_name(item.tag) != "Item":
                continue
            areas, kinds = [], []
            for child in item.iter():
                if local_name(child.tag) == "Area":
                    name = first_text(child, "Name")
                    if name:
                        areas.append(name)
                elif local_name(child.tag) == "Kind":
                    name = direct_child_text(child, "Name") or ""
                    status = direct_child_text(child, "Status") or ""
                    if "警報" in name and "注意報" not in name:
                        kinds.append((name, status))
            for area in dict.fromkeys(areas):
                for kind, status in kinds:
                    updates.append({
                        "area": area, "kind": kind, "status": status,
                        "updated_at": report_time,
                    })
    return updates


def apply_warning_updates(state: dict, updates: list[dict]) -> None:
    for update in updates:
        key = (update["area"], update["kind"])
        if "解除" in update["status"] or "取消" in update["status"]:
            state.pop(key, None)
        else:
            state[key] = update


def parse_typhoon_update(xml_bytes: bytes, source_xml: str = "") -> dict:
    root = ET.fromstring(xml_bytes)
    head = common_head(root)
    headline = head.get("headline") or ""
    return {
        "event_id": head.get("event_id") or source_xml,
        "title": head.get("title") or "台風情報",
        "time": head.get("target_time") or head.get("report_time"),
        "headline": headline or None,
        "active": not any(word in headline for word in END_TYPHOON_WORDS),
        "official_url": JMA_TYPHOON_PAGE,
        "source_xml": source_xml,
    }


def previous_warning_state(previous: dict) -> dict:
    return {
        (item["area"], item["kind"]): item
        for item in previous.get("_warning_state", [])
        if item.get("area") and item.get("kind")
    }


def previous_typhoon_state(previous: dict) -> dict:
    return {
        item["event_id"]: item
        for item in previous.get("_typhoon_state", [])
        if item.get("event_id")
    }


def should_full_sync(previous: dict, now: datetime) -> bool:
    last_full = parse_datetime(previous.get("last_full_sync_at"))
    checked = parse_datetime(previous.get("checked_at"))
    if last_full is None or checked is None:
        return True
    if now - checked.astimezone(JST) > timedelta(minutes=20):
        return True
    return now - last_full.astimezone(JST) > timedelta(hours=6)


def process_extra(entries: list[dict], warnings: dict, typhoons: dict, fetcher) -> None:
    for entry in entries:
        title = entry.get("title", "")
        is_warning = any(word in title for word in WARNING_TITLES)
        is_typhoon = any(word in title for word in TYPHOON_TITLE_WORDS)
        if not (is_warning or is_typhoon):
            continue
        try:
            payload = fetcher(entry["link"])
        except Exception:
            continue
        if is_warning:
            apply_warning_updates(warnings, parse_warning_updates(payload))
        if is_typhoon:
            update = parse_typhoon_update(payload, entry["link"])
            if update["active"]:
                typhoons[update["event_id"]] = update
            else:
                typhoons.pop(update["event_id"], None)


def process_quake(entries: list[dict], previous: dict | None, fetcher) -> dict | None:
    candidates = [
        entry for entry in entries
        if any(word in entry.get("title", "") for word in QUAKE_TITLES)
    ]
    for entry in reversed(candidates):
        try:
            return parse_earthquake(fetcher(entry["link"]), entry["link"])
        except Exception:
            continue
    return previous


def summarize_warnings(state: dict) -> dict:
    grouped = {}
    for item in state.values():
        grouped.setdefault(item["kind"], set()).add(item["area"])
    groups = [
        {"kind": kind, "areas": sorted(areas), "count": len(areas)}
        for kind, areas in sorted(grouped.items())
    ]
    return {
        "active_count": len(state),
        "groups": groups[:8],
        "official_url": JMA_WARNING_PAGE,
    }


def prune_typhoons(state: dict, now: datetime) -> None:
    for event_id, item in list(state.items()):
        event_time = parse_datetime(item.get("time"))
        if event_time and now - event_time.astimezone(JST) > timedelta(hours=24):
            state.pop(event_id, None)


def load_json(path: Path | None) -> dict:
    if path is None or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def build_realtime(previous: dict, fetcher: Callable[[str], bytes] = fetch_bytes) -> dict:
    now = datetime.now(JST).replace(microsecond=0)
    full_sync = should_full_sync(previous, now)
    warnings = {} if full_sync else previous_warning_state(previous)
    typhoons = {} if full_sync else previous_typhoon_state(previous)
    quake = None if full_sync else previous.get("earthquake")
    errors, successes = [], 0

    extra_feed = FEEDS["extra_long" if full_sync else "extra_high"]
    quake_feed = FEEDS["eqvol_long" if full_sync else "eqvol_high"]

    try:
        process_extra(parse_atom(fetcher(extra_feed)), warnings, typhoons, fetcher)
        successes += 1
    except Exception as exc:
        errors.append(f"extra: {type(exc).__name__}: {exc}")
        if full_sync:
            warnings = previous_warning_state(previous)
            typhoons = previous_typhoon_state(previous)

    try:
        quake = process_quake(parse_atom(fetcher(quake_feed)), quake, fetcher)
        successes += 1
    except Exception as exc:
        errors.append(f"eqvol: {type(exc).__name__}: {exc}")
        if full_sync:
            quake = previous.get("earthquake")

    prune_typhoons(typhoons, now)
    status = "ok" if not errors else ("partial" if successes else "degraded")
    checked_at = now.isoformat() if successes else (previous.get("checked_at") or now.isoformat())

    return {
        "schema_version": "1.0",
        "status": status,
        "checked_at": checked_at,
        "attempted_at": now.isoformat(),
        "last_full_sync_at": (
            now.isoformat() if full_sync and successes
            else previous.get("last_full_sync_at")
        ),
        "source": {"name": "気象庁", "url": JMA_PULL_PAGE},
        "earthquake": quake,
        "warnings": summarize_warnings(warnings),
        "typhoons": sorted(
            typhoons.values(), key=lambda item: item.get("time") or "", reverse=True
        )[:3],
        "_warning_state": sorted(warnings.values(), key=lambda x: (x["area"], x["kind"])),
        "_typhoon_state": sorted(typhoons.values(), key=lambda x: x.get("event_id") or ""),
        "errors": errors,
        "note": "当サイトの表示には遅延する場合があります。避難判断には気象庁・自治体などの最新情報を確認してください。",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_realtime(load_json(args.previous))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": result["status"],
        "checked_at": result["checked_at"],
        "warnings": result["warnings"]["active_count"],
        "typhoons": len(result["typhoons"]),
        "earthquake": bool(result["earthquake"]),
        "errors": result["errors"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
