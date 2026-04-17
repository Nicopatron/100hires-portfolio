# AI Tools Setup — 100Hires Portfolio

Nicolas Patron Uriburu · April 2026

---

## Tools Installed

| Tool | Version | Notes |
|------|---------|-------|
| Cursor | 3.1.14 | Already installed — VS Code fork, familiar environment |
| Claude Code | 2.1.109 (CLI + Cursor extension) | Daily driver — my primary dev environment for 6+ months |
| Codex | OpenAI's coding agent (Cursor extension) | Already installed from marketplace |

## Steps Completed

1. Opened Cursor, confirmed Claude Code and Codex extensions were installed
2. Logged into Claude Code — already authenticated from daily CLI usage
3. Created this public repository on GitHub
4. Wrote this README
5. Committed and pushed

## Issues and How I Solved Them

No significant issues. Claude Code, Cursor, and Codex were already part of my setup.

**Claude Code** has been my primary working environment since late 2024. I use it to build products, write content, research markets, and ship work autonomously — through the CLI, not just the IDE extension. This README, the repository, and the writing sample below were all produced in a Claude Code session.

## Writing Sample

As part of my application, I wrote a comparison page for 100Hires:

**[100Hires vs Greenhouse: Which ATS Is Better for Startups in 2026?](samples/100hires-vs-greenhouse.md)**

Researched, structured, written, and edited in one session using Claude Code. It's the kind of content I'd produce in this role — clear, honest, and built to help a reader make a decision.

---

## Step 2: Research Project

**Topic**: LinkedIn Organic Content Strategy for B2B SaaS

LinkedIn organic is the highest-leverage acquisition channel for a bootstrapped B2B SaaS with a small team. No ad spend, no months-long SEO ramp — just consistency, strategy, and compounding returns. I chose this topic because 100Hires could execute a playbook built from this research.

### Experts and Playbook Coverage

10 practitioners selected to cover the full cycle: strategy, creation, distribution, measurement.

| Dimension | Expert | Key credential |
|-----------|--------|---------------|
| Founder-led content system | Justin Welsh | $12.5M+ revenue, 800K+ followers, solopreneur |
| LinkedIn as revenue channel | Adam Robinson | $0→$25M ARR, LinkedIn as sole distribution |
| Growth frameworks / formatting | Lara Acosta | 200K+ followers, #1 fastest-growing female creator |
| Algorithm data / timing | Richard van der Blom | Annual Algorithm Insights Report, 1.5M+ posts analyzed |
| Measurement / ROI | Steffen Hedebrandt | CMO of Dreamdata, LinkedIn Ads Benchmarks Report |
| B2B demand gen strategy | Liam Moroney | CEO of Storyboard, dark social and brand-driven demand |
| B2B community + brand | Dave Gerhardt | Founded Exit Five (5,700+ members), ex-CMO Drift |
| Audience research | Amanda Natividad | VP Marketing at SparkToro, "Zero-Click Marketing" |
| Enterprise B2B content | Devin Reed | Scaled Gong content $20M→$200M ARR |
| Content distribution | Ross Simmonds | "Create Once, Distribute Forever," Foundation agency |

Full expert profiles with credentials, annotations, and links: [`research/sources.md`](research/sources.md)

### What's Collected

| Source | Method | Volume |
|--------|--------|--------|
| LinkedIn posts | Manual curation + [formatting script](tools/format-linkedin-posts.py) | 6–8 posts per expert, filtered by playbook relevance |
| YouTube transcripts | [`youtube-transcript-api`](tools/fetch-transcripts.py) | 2 videos per expert (20 total) — in progress |
| Supplementary materials | Manual synthesis | Algorithm report key findings |

### Directory Structure

```
research/
  sources.md                        # 10 experts: credentials, playbook dimension, links
  linkedin-posts/                   # 10 files, one per expert
  youtube-transcripts/              # ~20 transcripts (pending collection)
  other/                            # Algorithm report synthesis, frameworks
tools/
  fetch-transcripts.py              # YouTube transcript fetcher (youtube-transcript-api)
  format-linkedin-posts.py          # Apify JSON → markdown formatter
```

### Expert Selection Process

Started with 10 candidates covering distinct playbook dimensions. During collection, identified two weak slots through content quality review: Daniel Murray (too generic for rigorous measurement) and Chris Walker (pivoted away from B2B marketing in 2025). Replaced with Steffen Hedebrandt (hard attribution data) and Liam Moroney (demand gen theory) after cross-validating with multiple research tools. Reasoning documented in [`sources.md`](research/sources.md).

---

*Built with Claude Code.*
