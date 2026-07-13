#!/usr/bin/env python3
"""Build public companion pages from reviewed SRT files and a checked manifest.

The manifest is intentionally explicit: adding a YouTube upload does not make a
page public by itself. Before adding an entry, verify that the video is public,
rights are cleared, medical QA passed, and the referenced SRT is the final
human-reviewed caption track.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


SRT_BLOCK = re.compile(
    r"(?:^|\n)\d+\s*\n"
    r"\d{2}:\d{2}:\d{2},\d{3}\s+-->\s+\d{2}:\d{2}:\d{2},\d{3}\s*\n"
    r"(.*?)(?=\n\s*\n\d+\s*\n|\Z)",
    re.S,
)
SPEAKER = re.compile(r"^([^:]{1,30}):\s*(.*)$", re.S)


def scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def read_cues(path: Path) -> list[tuple[str, str]]:
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    cues: list[tuple[str, str]] = []
    for match in SRT_BLOCK.finditer(raw):
        text = " ".join(line.strip() for line in match.group(1).splitlines()).strip()
        speaker_match = SPEAKER.match(text)
        if speaker_match:
            speaker, text = speaker_match.groups()
        else:
            speaker = "Narrator"
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            cues.append((speaker.strip(), text))
    if not cues:
        raise ValueError(f"No usable caption cues found in {path}")
    return cues


def transcript_markdown(cues: list[tuple[str, str]], max_words: int = 150) -> str:
    paragraphs: list[tuple[str, str]] = []
    current_speaker = ""
    current_parts: list[str] = []
    current_words = 0

    def flush() -> None:
        nonlocal current_speaker, current_parts, current_words
        if current_parts:
            paragraphs.append((current_speaker, " ".join(current_parts)))
        current_speaker, current_parts, current_words = "", [], 0

    for speaker, text in cues:
        words = len(text.split())
        if current_parts and (speaker != current_speaker or current_words + words > max_words):
            flush()
        if not current_parts:
            current_speaker = speaker
        current_parts.append(text)
        current_words += words
    flush()
    return "\n\n".join(f"**{speaker}:** {text}" for speaker, text in paragraphs)


def front_matter(item: dict, digest: str) -> str:
    lines = [
        "---",
        "layout: episode",
        f"title: {scalar(item['title'])}",
        f"slug: {item['slug']}",
        f"exam: {scalar(item['exam'])}",
        f"description: {scalar(item['description'])}",
        f"video_id: {item['video_id']}",
        f"youtube_url: {item['youtube_url']}",
        f"upload_date: {item['upload_date']}",
        f"reviewed_date: {item['reviewed_date']}",
        f"duration: {item['duration']}",
        f"caption_sha256: {digest}",
        f"quick_answer: {scalar(item['quick_answer'])}",
        "faq:",
    ]
    for faq in item["faq"]:
        lines.extend([f"  - q: {scalar(faq['q'])}", f"    a: {scalar(faq['a'])}"])
    lines.append("sources:")
    lines.extend(f"  - {scalar(source)}" for source in item["sources"])
    lines.append("---")
    return "\n".join(lines)


def build_page(item: dict, media_root: Path, output_dir: Path) -> Path:
    required_gates = {
        "visibility": "public",
        "rights_cleared": True,
        "medical_qa": "pass",
        "captions_reviewed": True,
    }
    failed = {
        key: item.get(key)
        for key, expected in required_gates.items()
        if item.get(key) != expected
    }
    if failed:
        raise ValueError(f"Publication gates failed for {item.get('slug')}: {failed}")
    source = media_root / item["caption_source"]
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    transcript = transcript_markdown(read_cues(source))
    related = "\n".join(
        f"- [{video['title']}](https://youtu.be/{video['id']})" for video in item["related_public_videos"]
    )
    body = (
        f"{front_matter(item, digest)}\n\n"
        "This page mirrors the final reviewed English caption track of an original teaching video. "
        "It is for exam preparation and general medical education, not patient-specific medical advice.\n\n"
        "## Related public Shorts\n\n"
        f"{related or '_No related public Shorts._'}\n\n"
        "## Transcript\n\n"
        f"{transcript}\n"
    )
    output = output_dir / f"{item['slug']}.md"
    output.write_text(body, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--media-root", type=Path, required=True)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).with_name("public_episode_manifest.json"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "_episodes",
    )
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for item in manifest["episodes"]:
        print(build_page(item, args.media_root, args.output_dir))


if __name__ == "__main__":
    main()
