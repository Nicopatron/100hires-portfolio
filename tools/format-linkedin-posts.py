#!/usr/bin/env python3
"""
Format LinkedIn posts from Apify JSON output into markdown files.

Usage:
    python tools/format-linkedin-posts.py <apify-output.json>

Reads Apify JSON (from harvestapi/linkedin-profile-posts actor),
groups posts by author, and saves one markdown file per author
in research/linkedin-posts/.

The Apify actor config used:
    - Actor: harvestapi/linkedin-profile-posts
    - maxPosts: 10
    - postedLimit: "6months"
    - scrapeReactions: true
"""

import json
import os
import re
import sys
from datetime import datetime


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "research", "linkedin-posts")

# Map LinkedIn profile URLs to expert slugs and display names
EXPERT_MAP: dict[str, tuple[str, str]] = {
    "justinwelsh": ("justin-welsh", "Justin Welsh"),
    "retentionadam": ("adam-robinson", "Adam Robinson"),
    "laraacostar": ("lara-acosta", "Lara Acosta"),
    "richardvanderblom": ("richard-van-der-blom", "Richard van der Blom"),
    "daniel-murray-marketing": ("daniel-murray", "Daniel Murray"),
    "chriswalker171": ("chris-walker", "Chris Walker"),
    "davegerhardt": ("dave-gerhardt", "Dave Gerhardt"),
    "amandanat": ("amanda-natividad", "Amanda Natividad"),
    "devinreed": ("devin-reed", "Devin Reed"),
    "rosssimmonds": ("ross-simmonds", "Ross Simmonds"),
}


def extract_author_slug(post: dict) -> str | None:
    """Extract the LinkedIn username from post data to identify the author."""
    profile_url = post.get("authorProfileUrl", "") or post.get("profileUrl", "")
    if not profile_url:
        return None

    # Extract username from URL like https://www.linkedin.com/in/justinwelsh
    match = re.search(r"linkedin\.com/in/([^/?]+)", profile_url)
    if match:
        return match.group(1).rstrip("/")
    return None


def format_engagement(post: dict) -> str:
    """Format engagement metrics from a post."""
    parts = []
    likes = post.get("numLikes") or post.get("likesCount") or post.get("engagementCount", 0)
    comments = post.get("numComments") or post.get("commentsCount", 0)
    reposts = post.get("numReposts") or post.get("repostsCount", 0)

    if likes:
        parts.append(f"{likes:,} reactions")
    if comments:
        parts.append(f"{comments:,} comments")
    if reposts:
        parts.append(f"{reposts:,} reposts")

    return " | ".join(parts) if parts else "No engagement data"


def format_date(post: dict) -> str:
    """Extract and format the post date."""
    date_str = post.get("postedDate") or post.get("postedAt") or post.get("timestamp", "")
    if not date_str:
        return "Date unknown"

    # Try parsing ISO format
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        pass

    return str(date_str)[:10] if date_str else "Date unknown"


def save_author_file(
    slug: str,
    display_name: str,
    profile_url: str,
    posts: list[dict],
) -> str:
    """Save all posts for one author as a markdown file."""
    filename = f"{slug}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Sort posts by date (newest first)
    posts.sort(key=lambda p: format_date(p), reverse=True)

    dates = [format_date(p) for p in posts]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "Unknown"

    lines = [
        f"# {display_name} — LinkedIn Posts\n",
        f"- **Profile**: {profile_url}",
        f"- **Posts collected**: {len(posts)}",
        f"- **Date range**: {date_range}",
        f"- **Collection method**: Apify (harvestapi/linkedin-profile-posts)",
        "",
        "---",
        "",
    ]

    for i, post in enumerate(posts, 1):
        text = post.get("text") or post.get("postText") or post.get("content", "")
        text = text.strip()

        if not text:
            continue

        date = format_date(post)
        engagement = format_engagement(post)
        post_url = post.get("postUrl") or post.get("url", "")

        lines.append(f"## Post {i} — {date}\n")
        if post_url:
            lines.append(f"[View on LinkedIn]({post_url})\n")
        lines.append(f"**Engagement**: {engagement}\n")
        lines.append(text)
        lines.append("")
        lines.append("---")
        lines.append("")

    content = "\n".join(lines)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def main():
    if len(sys.argv) < 2:
        print("Usage: python format-linkedin-posts.py <apify-output.json>")
        print("\nExpects JSON output from Apify actor: harvestapi/linkedin-profile-posts")
        sys.exit(1)

    input_path = sys.argv[1]

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"Expected a JSON array, got {type(data).__name__}")
        sys.exit(1)

    print(f"Loaded {len(data)} posts from {input_path}\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Group posts by author
    grouped: dict[str, list[dict]] = {}
    unmatched = 0

    for post in data:
        username = extract_author_slug(post)
        if username and username in EXPERT_MAP:
            grouped.setdefault(username, []).append(post)
        else:
            unmatched += 1

    if unmatched:
        print(f"Warning: {unmatched} posts couldn't be matched to a known expert\n")

    # Save one file per author
    for username, posts in grouped.items():
        slug, display_name = EXPERT_MAP[username]
        profile_url = f"https://www.linkedin.com/in/{username}/"
        path = save_author_file(slug, display_name, profile_url, posts)
        print(f"  Saved: {os.path.basename(path)} ({len(posts)} posts)")

    found_experts = len(grouped)
    expected = len(EXPERT_MAP)
    print(f"\nDone. {found_experts}/{expected} experts with posts saved.")

    missing = set(EXPERT_MAP.keys()) - set(grouped.keys())
    if missing:
        print(f"Missing: {', '.join(EXPERT_MAP[u][1] for u in missing)}")


if __name__ == "__main__":
    main()
