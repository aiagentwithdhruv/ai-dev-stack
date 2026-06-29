---
title: Three Knowledge Streams
type: architecture
---

# Three Knowledge Streams

All knowledge entering the learning hub comes from one of three sources. Knowing which stream a piece of knowledge belongs to tells you where to route it, how to format it, and how long it stays relevant.

---

## Stream 1 — Internal

**What it is:** Everything you learn by doing. Errors, fixes, patterns that work, patterns that fail, build logs, deployment gotchas, schema decisions.

**Where it lives:**
- `LEARNING-ZONE.md` — the live log of errors and fixes (read at every session start)
- `techniques/` — stable, reusable patterns extracted from experience
- `ERRORS.md` (project root) — a global error log, synced with LEARNING-ZONE

**What belongs here:**

| Content type | Where it goes |
|---|---|
| Bug → cause → fix | LEARNING-ZONE.md immediately |
| Pattern that worked across 3+ uses | New file in techniques/ |
| Deployment gotcha | LEARNING-ZONE.md + techniques/deployment-*.md |
| Schema decision with reasoning | techniques/ relevant file |
| Build log observation | LEARNING-ZONE.md |

**Routing rule:** If you learned it by running your own code, it is Internal. Write it within the session. Do not defer — context evaporates.

**Freshness:** Internal knowledge is the most reliable. It reflects what is actually true in your codebase right now. Technique files from this stream rarely go stale faster than the codebase itself.

---

## Stream 2 — External

**What it is:** What the world is doing. Industry news, model releases, competitor moves, framework updates, research papers, benchmarks.

**Where it lives:**
- `daily/` — daily intelligence briefs (one per day)
- `market/` — industry vertical files (manufacturing-erp, voice-ai, agent-frameworks, etc.)
- `competitors/` — one file per competitor, updated as news arrives

**What belongs here:**

| Content type | Where it goes |
|---|---|
| Model release (Claude, GPT, Gemini) | daily brief + techniques/ update if behavior-changing |
| Framework update (LangGraph, CrewAI) | daily brief + techniques/agent-frameworks-comparison.md |
| Competitor feature ship | competitors/[name].md |
| Research paper with actionable findings | daily brief + new technique file if substantial |
| Pricing change (cloud, API) | daily brief + relevant technique file |
| Benchmark result | market/[vertical].md |

**Routing rule:** If it comes from outside your codebase, it is External. Route it based on whether it is time-sensitive (daily brief) or evergreen (market or technique file).

**Freshness:** External knowledge decays. Model benchmarks are obsolete in 3 months. Competitor intel in 6. Tag every External entry with a date. During weekly lint, flag entries older than 60 days for review.

---

## Stream 3 — Curated

**What it is:** What the human drops in manually. Articles, screenshots, voice recordings, video links, WhatsApp forwards, pulled quotes, bookmarks. This stream does not arrive on a schedule — it arrives whenever the human notices something worth keeping.

**Where it lives:**
- `feed/inbox/` — raw drop zone, unprocessed
- Processed output routes to `techniques/`, `market/`, `competitors/`, or `daily/` depending on content type

**What belongs here:**

| Content type | Processing action |
|---|---|
| Article link | Fetch, summarize, route to market/ or techniques/ |
| Voice recording | Transcribe (see video-transcript-workflow.md), extract key points, route |
| Video / podcast link | Auto-sub via yt-dlp or fallback to Whisper, then same as above |
| Screenshot | OCR if needed, describe content, route |
| Raw note / thought | Assess fit, route to technique/ or LEARNING-ZONE |

**Routing rule:** If the human explicitly put it there, it is Curated. Process it the same session it arrives — do not let the inbox accumulate more than 10 items unprocessed.

**Freshness:** Varies. Articles from 6 months ago can still contain durable patterns. The date stamps in the frontmatter let you judge.

---

## The Routing Diagram

```
INTERNAL               EXTERNAL               CURATED
(what you build)       (what the world does)  (what you drop in)

session error         model release           article link
  |                     |                       |
  v                     v                       v
LEARNING-ZONE.md      daily brief            feed/inbox/
  |                     |                       |
  +---------- techniques/ <--------------------+
                    |
                    v
              market/
              competitors/
              (if relevant to a vertical or competitor)
```

---

## Stream interaction

The streams interact. An external paper (Stream 2) that validates what you learned from experience (Stream 1) should produce a technique update that cites both. A curated article (Stream 3) that contradicts an existing technique should trigger a technique revision, not a new file.

The hub has one version of the truth per topic. When streams conflict, Internal (what actually happened in your codebase) beats External (what a paper or blog claims) on implementation questions. External beats Internal on market and pricing questions (you have no first-hand data there). Curated helps you discover what you do not know to look for.

---

## Lint discipline

Once a week, review each stream for drift:

- **Internal:** Are technique files still accurate given recent code changes? Flag stale entries in LEARNING-ZONE.
- **External:** Are market files and competitor files still current? Delete what is obviously obsolete.
- **Curated:** Is the inbox empty? Process anything that accumulated.

The lint is not a deep review — it is a 20-minute scan. The goal is to ensure the hub remains a source of truth, not an archive of what was once true.
