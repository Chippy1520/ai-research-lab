#!/usr/bin/env python3
"""Live-check every curriculum video against YouTube oEmbed.

Static tests validate schema and coverage without depending on the network. Run this
script whenever curriculum_resources.json changes; it verifies that every selected
watch URL still resolves and that the stored title/author match YouTube's response.
"""

from __future__ import annotations

import concurrent.futures
import html
import json
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_PATH = ROOT / "curriculum_resources.json"
CTX = ssl.create_default_context()
SOURCE_TYPES = {
    "university_course",
    "research_lab",
    "official_conference",
    "professional_foundation",
    "respected_educator",
}


def fetch_oembed(url: str) -> dict[str, Any]:
    endpoint = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url, safe="")
    request = urllib.request.Request(endpoint, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, context=CTX, timeout=20) as response:
        return json.load(response)


def check_video(video: dict[str, Any]) -> tuple[str, list[str]]:
    url = video["url"]
    errors: list[str] = []
    try:
        payload = fetch_oembed(url)
    except Exception as exc:  # network and HTTP failures are both actionable here
        return url, [f"oEmbed failed: {exc}"]

    actual_title = html.unescape(str(payload.get("title", ""))).strip()
    actual_author = html.unescape(str(payload.get("author_name", ""))).strip()
    if actual_title != video["title"]:
        errors.append(f"title mismatch: stored={video['title']!r}, live={actual_title!r}")
    if actual_author != video["author"]:
        errors.append(f"author mismatch: stored={video['author']!r}, live={actual_author!r}")
    return url, errors


def main() -> int:
    payload = json.loads(RESOURCE_PATH.read_text(encoding="utf-8"))
    videos = [video for lesson in payload["lessons"] for video in lesson["videos"]]
    static_errors: list[str] = []
    for lesson in payload["lessons"]:
        orders = [int(video["order"]) for video in lesson["videos"]]
        if not lesson["videos"] and lesson.get("selection_status") != "deferred_until_topic_selected":
            static_errors.append(f"Day {lesson['day']:02d}: no videos without an explicit deferred frontier topic")
        if lesson["videos"] and lesson.get("selection_status") != "verified":
            static_errors.append(f"Day {lesson['day']:02d}: videos exist but selection is not marked verified")
        if orders != list(range(1, len(orders) + 1)):
            static_errors.append(f"Day {lesson['day']:02d}: non-contiguous video order {orders}")
        for video in lesson["videos"]:
            if video.get("language") != "English":
                static_errors.append(f"Day {lesson['day']:02d}: non-English marker for {video['url']}")
            if video.get("source_type") not in SOURCE_TYPES:
                static_errors.append(f"Day {lesson['day']:02d}: unsupported source_type for {video['url']}")
            if not video.get("source_rationale"):
                static_errors.append(f"Day {lesson['day']:02d}: missing source rationale for {video['url']}")

    unique = {video["url"]: video for video in videos}
    live_errors: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(check_video, video) for video in unique.values()]
        for future in concurrent.futures.as_completed(futures):
            url, errors = future.result()
            live_errors.extend(f"{url}: {error}" for error in errors)

    errors = static_errors + live_errors
    if errors:
        print("Curriculum video verification FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Verified {len(videos)} curriculum placements across "
        f"{len(unique)} live YouTube videos; stored titles/authors match oEmbed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
