# Tools

Scripts used to collect and format research material for Step 2.

## Setup

```bash
pip install -r ../requirements.txt
```

Python 3.9+ required. Scripts are run from the repo root.

---

## `fetch-transcripts.py`

Fetches YouTube transcripts via the public `youtube-transcript-api` and saves them as markdown files with metadata headers.

- **Dependencies**: `youtube-transcript-api>=0.6.0`
- **Input**: hardcoded `VIDEOS` dict at top of script (expert → list of `(video_id, title, channel, date, duration)`)
- **Output**: `research/youtube-transcripts/{expert-slug}--{title-slug}.md` — one file per video, with metadata header

```bash
python tools/fetch-transcripts.py
```

Expected output:
```
Fetching transcripts for 20 videos across 10 experts...

[justin-welsh]
  Saved: justin-welsh--how-i-built-an-8m-business-with-0-employees.md
  Saved: justin-welsh--why-i-built-a-non-scalable-7-figure-business.md
...

Done. 20/20 transcripts saved, 0 failed.
```

Notes:
- 10-second sleep between requests to avoid YouTube IP rate-limiting
- Videos without captions will fail gracefully (failure count shown at end)
- Transcripts are saved as single-line text; run `chunk-transcripts.py` after to paragraph-format them

---

## `chunk-transcripts.py`

Rewrites each `research/youtube-transcripts/*.md` in place — preserves the metadata header and splits the body into ~500-char paragraphs at sentence boundaries (hard limit at 1,000 chars when punctuation is sparse).

- **Dependencies**: stdlib only
- **Input**: existing `research/youtube-transcripts/*.md` files
- **Output**: same files, rewritten with paragraph breaks

```bash
python tools/chunk-transcripts.py
```

Expected output:
```
Chunking 20 transcripts in research/youtube-transcripts

  {filename}.md: N paragraphs (N chars)
  ...

Done. 1193 paragraphs across 20 files.
```

---

## `format-linkedin-posts.py`

Parses JSON output from the Apify `harvestapi/linkedin-profile-posts` actor and writes one markdown file per author under `research/linkedin-posts/`.

- **Dependencies**: stdlib only
- **Input**: Apify JSON file (array of post objects with `authorProfileUrl`, `text`, `postedDate`, `numLikes`, etc.)
- **Output**: `research/linkedin-posts/{expert-slug}.md` — one file per matched author, sorted by date (newest first)

```bash
python tools/format-linkedin-posts.py <apify-output.json>
```

Expected output:
```
Loaded N posts from apify-output.json

  Saved: justin-welsh.md (7 posts)
  Saved: adam-robinson.md (7 posts)
  ...

Done. 10/10 experts with posts saved.
```

Notes:
- `EXPERT_MAP` dict at top of script maps LinkedIn usernames to expert slugs; edit to add/remove authors
- Warns on posts that don't match any known expert
- Profiles beyond Apify quota were collected manually via the Claude Chrome extension — this formatting script is source-agnostic once JSON is available in the expected shape

[← Back to repo root](../README.md)
