# Research — LinkedIn Organic Content Strategy for B2B SaaS

Research collection for Step 2 of the 100Hires Growth Marketing hiring process. 10 experts × curated LinkedIn posts + YouTube transcripts + highlights, plus cross-expert synthesis.

## Structure

| Folder / File | What's in it |
|---|---|
| [`sources.md`](sources.md) | 10 experts with credentials, playbook dimension, LinkedIn + YouTube links, collection method, and annotation |
| [`linkedin-posts/`](linkedin-posts/) | 10 files — one per expert. 6–8 curated posts each, with engagement data and selection criteria |
| [`youtube-transcripts/`](youtube-transcripts/) | 20 files — 2 transcripts per expert, paragraph-chunked for readability |
| [`highlights/`](highlights/) | 10 files — 5–7 high-signal quotes per expert, with source citations and strategic implication |
| [`other/linkedin-algorithm-2024-2026-key-findings.md`](other/linkedin-algorithm-2024-2026-key-findings.md) | Synthesis of Richard van der Blom's Algorithm Insights Reports (2024, 2026) |
| [`other/playbook-synthesis.md`](other/playbook-synthesis.md) | Cross-expert synthesis across 8 playbook dimensions + identified coverage gap |

## Suggested reading order

1. **[`sources.md`](sources.md)** — who the 10 experts are and why each was selected
2. **[`other/playbook-synthesis.md`](other/playbook-synthesis.md)** — cross-expert synthesis, agreement/disagreement, and the identified gap
3. **[`highlights/`](highlights/)** — dive into specific experts whose dimensions matter for your playbook
4. **[`linkedin-posts/`](linkedin-posts/) and [`youtube-transcripts/`](youtube-transcripts/)** — raw source material for quote verification

## Collection methods

- LinkedIn posts: Apify (`harvestapi/linkedin-profile-posts`) + Claude Chrome extension fallback for profiles beyond Apify quota
- YouTube transcripts: [`youtube-transcript-api`](https://github.com/jdepoix/youtube-transcript-api) via [`../tools/fetch-transcripts.py`](../tools/fetch-transcripts.py)
- Transcript chunking: [`../tools/chunk-transcripts.py`](../tools/chunk-transcripts.py)

See [`../tools/README.md`](../tools/README.md) for how to reproduce.

[← Back to repo root](../README.md)
