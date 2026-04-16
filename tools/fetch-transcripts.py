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
from datetime import datetime

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Install dependency: pip install youtube-transcript-api")
    sys.exit(1)


# Videos to fetch — organized by expert
# Format: "expert-slug": [("video-id", "title", "channel", "date", "duration")]
VIDEOS: dict[str, list[tuple[str, str, str, str, str]]] = {
    # Populate with actual video IDs after research
    # Example:
    # "justin-welsh": [
    #     ("dQw4w9WgXcQ", "How I Built a $10M LinkedIn Business", "My First Million", "2024-06-15", "45:22"),
    # ],
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
            text = snippet.get("text", "").strip()
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

    print(f"\nDone. {fetched}/{total} transcripts saved, {failed} failed.")
    if failed:
        print("Tip: failed videos may not have captions. Try Apify as fallback.")


if __name__ == "__main__":
    main()
