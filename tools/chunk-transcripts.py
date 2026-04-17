#!/usr/bin/env python3
"""
Chunk YouTube transcript bodies into paragraphs for human readability.

YouTube auto-captions are fetched as one continuous string. This script
rewrites each research/youtube-transcripts/*.md file in place, preserving
the metadata header and splitting the body into ~500-char paragraphs at
sentence boundaries where possible, or at word boundaries as fallback.

Usage:
    python tools/chunk-transcripts.py
"""

import re
import sys
from pathlib import Path


TRANSCRIPTS_DIR = Path(__file__).parent.parent / "research" / "youtube-transcripts"
TARGET_CHARS = 500
HARD_LIMIT_MULT = 2
SENTENCE_END = re.compile(r"[.!?]$")


def split_header_body(content: str) -> tuple[str, str]:
    """Split file at the first '---' separator line that closes the metadata block."""
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.strip() == "---" and i > 0:
            header = "\n".join(lines[: i + 1])
            body = "\n".join(lines[i + 1 :]).strip()
            return header, body
    return content, ""


def chunk_body(body: str, target: int = TARGET_CHARS) -> str:
    """Group words into paragraphs at sentence boundaries when possible."""
    body = re.sub(r"\s+", " ", body).strip()
    if not body:
        return ""

    words = body.split(" ")
    paragraphs: list[str] = []
    buf: list[str] = []
    chars = 0
    hard_limit = target * HARD_LIMIT_MULT

    for word in words:
        buf.append(word)
        chars += len(word) + 1

        if chars >= target and SENTENCE_END.search(word):
            paragraphs.append(" ".join(buf))
            buf, chars = [], 0
        elif chars >= hard_limit:
            paragraphs.append(" ".join(buf))
            buf, chars = [], 0

    if buf:
        paragraphs.append(" ".join(buf))

    return "\n\n".join(paragraphs)


def process_file(path: Path) -> tuple[int, int]:
    """Rewrite one transcript. Returns (paragraphs_created, body_chars)."""
    content = path.read_text(encoding="utf-8")
    header, body = split_header_body(content)
    if not body:
        return 0, 0
    chunked = chunk_body(body)
    path.write_text(header + "\n\n" + chunked + "\n", encoding="utf-8")
    return chunked.count("\n\n") + 1, len(body)


def main() -> int:
    files = sorted(TRANSCRIPTS_DIR.glob("*.md"))
    if not files:
        print(f"No transcripts in {TRANSCRIPTS_DIR}")
        return 1

    print(f"Chunking {len(files)} transcripts in {TRANSCRIPTS_DIR}\n")
    total_paragraphs = 0
    for path in files:
        paragraphs, chars = process_file(path)
        total_paragraphs += paragraphs
        print(f"  {path.name}: {paragraphs} paragraphs ({chars:,} chars)")

    print(f"\nDone. {total_paragraphs} paragraphs across {len(files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
