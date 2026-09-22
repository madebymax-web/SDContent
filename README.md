# Finest City Facts — San Diego Faceless Content Engine

An automated pipeline for a faceless YouTube Shorts / Instagram Reels /
long-form YouTube channel about interesting, verified facts about San Diego.
No on-camera presenter — a consistent narration voice, visual style, and
research process *is* the channel.

Working name: **Finest City Facts** (see `docs/01-brand-strategy.md` for
alternatives and the reasoning — confirm handle availability before you
launch).

## Start here

Read the docs in order — each builds on the last:

| Doc | Covers |
|---|---|
| [`docs/01-brand-strategy.md`](docs/01-brand-strategy.md) | Name options, positioning, audience, tone, visual identity |
| [`docs/02-content-strategy.md`](docs/02-content-strategy.md) | Content pillars, formats, hook framework, platform adaptation, growth |
| [`docs/03-style-guide.md`](docs/03-style-guide.md) | Visual style, captions, voice, music, thumbnails |
| [`docs/04-production-pipeline.md`](docs/04-production-pipeline.md) | **The architecture** — why real footage over AI-generated scenes, full pipeline diagram, tool stack |
| [`docs/05-fact-sourcing-and-verification.md`](docs/05-fact-sourcing-and-verification.md) | How facts get sourced, verified, and gated before production |
| [`docs/06-legal-and-compliance.md`](docs/06-legal-and-compliance.md) | AI disclosure rules, footage/music licensing, ToS, channel settings |
| [`docs/07-monetization-and-growth.md`](docs/07-monetization-and-growth.md) | YPP, IG monetization, cross-promo plan, KPI tracking |
| [`docs/08-daily-operations-sop.md`](docs/08-daily-operations-sop.md) | Daily/weekly/monthly operating checklist |
| [`docs/09-roadmap.md`](docs/09-roadmap.md) | **Phased rollout** — what to do this week vs. later |

**If you only read one doc before deciding whether this framework is right,
read docs/04** — it explains the single biggest architectural decision
(real stock footage + TTS vs. fully AI-generated video) and why the
pipeline defaults the way it does.

## What's actually built vs. what needs your input

**Built and ready to use:**
- Full strategic framework (all of `docs/`)
- A seed fact database of 35 real San Diego facts, sourced and status-tracked
  (`data/facts_database.csv`)
- Script/production templates (`templates/`)
- LLM prompt templates for script-writing, topic research, and fact
  verification (`prompts/`)
- A working Python pipeline scaffold — topic selection, script generation
  (Anthropic API), TTS, visual sourcing (Pexels), ffmpeg assembly, caption
  burning, and publishing to YouTube/Instagram (`pipeline/`)
- A GitHub Actions workflow scaffold for scheduled, unattended runs
  (`.github/workflows/daily-content.yml`)

**Needs your input before it can actually run** (see `docs/09-roadmap.md`
Phase 0 for the full checklist):
- Confirm/register the channel name and handles
- API keys: Anthropic, ElevenLabs (or decide to use the Higgsfield voice
  already available in this workspace instead), Pexels/Pixabay
- YouTube channel + Google Cloud OAuth credentials
- Instagram Professional account + Meta App Review (budget 1-2 weeks — start
  this early, it's the longest lead-time item)
- Pick and lock a narration voice ID
- Brand assets: logo/wordmark/watermark, thumbnail template (Adobe Express is
  already connected in this workspace and is a strong fit for this)
- A place to grow the fact database beyond the 35-fact seed — 2-3 weeks of
  buffer is the target (docs/08)

## Quickstart (once API keys exist)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your keys
# edit config/channel_config.yaml: voice.voice_id at minimum

python -m pipeline.orchestrator --mode daily
```

This produces one Short end-to-end and drops it in `data/review_queue/` for
approval (review-gated by default — see `docs/04` for the automation
phase-out plan and `config/channel_config.yaml`'s `automation.review_required`).

## Repo map

```
docs/           strategy, style, pipeline architecture, legal, ops, roadmap
data/           facts database + content calendar template (+ review_queue/, gitignored output)
templates/      human-readable script structure references
prompts/        LLM system prompts used by pipeline/script_writer.py etc.
pipeline/       the actual Python pipeline (topic -> script -> voice -> visuals -> assemble -> caption -> publish)
config/         channel_config.yaml (non-secret settings)
.github/workflows/  scheduled pipeline run
assets/cache/   local working directory for in-progress renders (gitignored)
```

## A few things worth flagging (the "what am I overseeing" ask)

- **AI content disclosure policy** (docs/06): if you ever lean on
  photorealistic AI-generated video of real San Diego places, YouTube/Meta
  require a disclosure label. The default pipeline (real footage + TTS)
  avoids this question entirely — worth understanding *why* before anyone on
  your team reaches for a "just generate the B-roll" shortcut later.
- **Fact verification is a hard gate, not a suggestion** (docs/05) — the
  fastest way to lose a facts channel's entire value proposition is
  publishing something wrong. The pipeline enforces `status=verified` before
  a fact can be scripted; don't bypass it under deadline pressure.
- **Instagram's Meta App Review has real lead time** — start that process in
  Phase 0 even before content is ready, or it becomes the bottleneck for
  your Instagram launch date.
- **Music licensing** — easy to overlook, expensive to fix after the fact
  (a copyright claim can retroactively affect monetization across the whole
  channel). Stick to the royalty-free sources named in docs/03/06.
- **The review queue is deliberately not zero-touch at launch**, even though
  you asked for full automation — docs/04 explains the phase-out plan and
  why a few weeks of human review de-risks the "wrong fact goes out
  unattended" failure mode before removing it.
