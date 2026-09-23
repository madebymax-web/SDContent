# Roadmap

## Phase 0 — Setup (this week)

- [ ] Lock channel name/handles (docs/01) and register them on YouTube,
      Instagram, and defensively on TikTok.
- [ ] Create channel branding assets: logo/wordmark, watermark, intro
      stinger, thumbnail template (Adobe Express, already available in this
      workspace, is a good fit for this).
- [ ] Set up API access: Anthropic API key (script gen), ElevenLabs account +
      voice pick (or confirm using Higgsfield TTS instead), Pexels/Pixabay
      API keys (free tier).
- [ ] Set up YouTube channel (mark not-made-for-kids per docs/06), Instagram
      Professional account linked to a Facebook Page (needed for Graph API).
- [ ] Register a Google Cloud project + OAuth credentials for YouTube Data
      API; start the Meta App Review process for Instagram publishing early
      — this can take 1-2 weeks, start it even before content is ready.
- [ ] Fill in `.env` from `.env.example`.

## Phase 1 — MVP pipeline, manual-assisted (weeks 1-2)

- [ ] Seed `data/facts_database.csv` beyond the starter 30 (this repo ships
      a verified starter set — grow it to 2-3 weeks of buffer).
- [ ] Run the pipeline stages manually end-to-end for the first 5-10 videos
      to validate each stage's output quality before trusting it unattended:
      script tone, voice quality, visual/caption sync, color grade.
- [ ] Publish manually while validating; review queue is 100% required at
      this phase (docs/04).
- [ ] Get first 2-3 long-form videos out to validate the compilation format.

## Phase 2 — Automated pipeline, human review gate (weeks 3-8)

- [ ] Wire up `.github/workflows/daily-content.yml` to run the pipeline on
      schedule, landing renders in the review queue automatically.
- [ ] Move review queue into Notion (already connected in this workspace)
      for a better daily-review UX than flat files.
- [ ] Daily shorts cadence live; weekly long-form cadence live.
- [ ] Start tracking KPIs weekly per docs/07.
- [ ] Apply for YPP the moment thresholds are hit.

## Phase 3 — Reduce the review gate (weeks 9+)

- [ ] Per docs/04's phase-out plan: move from full review → spot-check →
      fully unattended, once the verification gate has a track record.
- [ ] Start the "one long-form → 3-5 shorts" repurposing workflow via
      Higgsfield Shorts Studio.
- [ ] Begin light cross-promotion per docs/07 phase 2, if follower
      milestones are hit.

## Phase 4 — Scale & expand (month 3+)

- [ ] Evaluate adding TikTok (same asset, per your platform decision to
      start with Shorts/Reels/long-form first and add TikTok later if it's
      worth the extra publishing integration).
- [ ] Evaluate sponsorships/local business partnerships once reach supports
      it (docs/07).
- [ ] Evaluate merch (Shopify already connected) if community demand shows
      up in comments/DMs.
- [ ] Revisit whether a second, purely-animated Higgsfield-based channel
      (flagged as an option in docs/04) is worth building as a companion
      property, now that the pipeline pattern is proven once.
- [ ] Full monthly strategy review against original docs/02 thesis — what's
      actually working vs. what was assumed at launch, and adjust.

## Immediate next step

Once you're happy with this framework, the next concrete build task is
Phase 0's API/account setup — none of that can be done inside this session
(needs your logins/payment methods), but I can generate the first batch of
scripts/videos in dry-run/mock mode against the scaffolding here to prove
the pipeline logic before any real accounts exist, if useful.
