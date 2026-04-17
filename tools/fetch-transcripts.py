#!/usr/bin/env python3
"""
Fetch YouTube transcripts and save as markdown files.

Usage:
    python tools/fetch-transcripts.py

Reads video list from VIDEOS dict below. Outputs markdown files to
research/youtube-transcripts/ with metadata headers.

Requires: pip install youtube-transcript-api
"""

import os
import re
import sys
import time
from datetime import datetime

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Install dependency: pip install youtube-transcript-api")
    sys.exit(1)


# Videos to fetch — organized by expert
# Format: "expert-slug": [("video-id", "title", "channel", "date", "duration")]
# Dates verified via yt-dlp against YouTube upload_date metadata.
VIDEOS: dict[str, list[tuple[str, str, str, str, str]]] = {
    "justin-welsh": [
        ("ZkwYxYfkfYU", "How I Built an $8M Business with 0 Employees", "Behind the Craft (Peter Yang)", "2024-09-15", "43:00"),
        ("Mp8m-ysmfq4", "Why I Built a Non-Scalable 7-Figure Business", "ActiveCampaign", "2025-12-02", "67:00"),
    ],
    "adam-robinson": [
        ("Xihp-uWZFaQ", "Adam Robinson Shares P&L, $22M Revenue, Strategy Behind LinkedIn", "Nathan Latka", "2024-10-17", "19:00"),
        ("U7JNHexncUw", "From Credit Trader to $25M ARR and RB2B Growth", "Product Growth", "2025-01-24", "146:00"),
    ],
    "lara-acosta": [
        ("ZK-CBIFDR9w", "I Blew Up My LinkedIn Following As Fast As I Could", "Lara Acosta", "2024-07-28", "18:00"),
        ("JmZYLO5yGiQ", "Watch Me Use AI to Create 30 Days of Viral LinkedIn Posts", "Lara Acosta", "2024-12-19", "10:00"),
    ],
    "richard-van-der-blom": [
        ("2BWpIPHpQG4", "The LinkedIn Algorithm in 2024 with Richard van der Blom", "Dreamdata", "2024-02-28", "55:00"),
        ("nmPGcQvDnEg", "How to Use LinkedIn 2025 Algorithm to Attract Clients", "Mark Whitby", "2025-06-27", "38:00"),
    ],
    "steffen-hedebrandt": [
        ("GTVYm4voyNw", "How to Attribute B2B Marketing Activities to Revenue", "SaaS Marketing Superstars", "2023-02-27", "36:00"),
        ("H0200CMTxg4", "Contrarian Growth Playbook and B2B Revenue Attribution", "FINITE B2B Marketing", "2025-10-27", "30:00"),
    ],
    "liam-moroney": [
        ("LuXuVv-ScCY", "The Dangers of Wrong-Termism with Liam Moroney", "Marketing Architects", "2025-07-22", "42:00"),
        ("2fQW3baHeVQ", "Developing An Allbound Marketing Ethos", "Wix Studio", "2025-02-19", "50:00"),
    ],
    "dave-gerhardt": [
        ("bGbPr6Z473o", "Building a Personal Brand as a Founder", "Finn Thormeier", "2025-03-06", "53:00"),
        ("1hJBQpFGlrg", "The Brand Flywheel: Authentic Content, Audience and Momentum", "AirOps", "2026-02-12", "55:00"),
    ],
    "amanda-natividad": [
        ("jW8oVoeHKqw", "Your Audience Your Edge: Unpacking Zero-Click Marketing", "Advanced Web Ranking", "2025-04-22", "48:00"),
        ("J98cUdZl-JQ", "What Zero Click Marketing Actually Is", "Amanda Natividad", "2026-03-10", "14:00"),
    ],
    "devin-reed": [
        ("FCcXQD9Rj_c", "Enterprise Content Strategy at Scale", "Podcast Interview", "2021-09-30", "27:00"),
        ("Hgl37lTOCs8", "Gong Content Playbook with Devin Reed", "Podcast Interview", "2024-06-13", "37:00"),
    ],
    "ross-simmonds": [
        ("GLXu57IrRQ8", "Create Once Distribute Forever with Ross Simmonds", "The Content Studio", "2024-02-23", "65:00"),
        ("lCypg4hUPBc", "B2B Content Distribution Masterclass", "EventShark TV", "2025-04-17", "52:00"),
    ],
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "research", "youtube-transcripts")


def slugify(text: str) -> str:
    """Convert text to a filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def fetch_transcript(video_id: str) -> str | None:
    """Fetch transcript text for a YouTube video. Returns None on failure."""
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)
        lines = []
        for snippet in transcript:
            text = (getattr(snippet, "text", "") or "").strip()
            if text:
                lines.append(text)
        return " ".join(lines)
    except Exception as e:
        print(f"  Failed to fetch transcript for {video_id}: {e}")
        return None


def save_transcript(
    expert_slug: str,
    video_id: str,
    title: str,
    channel: str,
    date: str,
    duration: str,
    transcript_text: str,
) -> str:
    """Save transcript as markdown file. Returns the output path."""
    filename = f"{expert_slug}--{slugify(title)}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    content = f"""# {title}

- **Expert**: {expert_slug.replace("-", " ").title()}
- **Channel**: {channel}
- **Date**: {date}
- **Duration**: {duration}
- **URL**: https://www.youtube.com/watch?v={video_id}
- **Collection method**: youtube-transcript-api (auto-generated captions)

---

{transcript_text}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def main():
    if not VIDEOS:
        print("No videos configured. Add video IDs to the VIDEOS dict in this script.")
        print("See comments in the source for the expected format.")
        sys.exit(0)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = sum(len(vids) for vids in VIDEOS.values())
    fetched = 0
    failed = 0

    print(f"Fetching transcripts for {total} videos across {len(VIDEOS)} experts...\n")

    for expert_slug, videos in VIDEOS.items():
        print(f"[{expert_slug}]")
        for video_id, title, channel, date, duration in videos:
            transcript_text = fetch_transcript(video_id)
            if transcript_text:
                path = save_transcript(
                    expert_slug, video_id, title, channel, date, duration, transcript_text
                )
                print(f"  Saved: {os.path.basename(path)}")
                fetched += 1
            else:
                failed += 1
            time.sleep(10)  # avoid YouTube IP rate limiting

    print(f"\nDone. {fetched}/{total} transcripts saved, {failed} failed.")
    if failed:
        print("Tip: failed videos may not have captions. Try Apify as fallback.")


if __name__ == "__main__":
    main()
