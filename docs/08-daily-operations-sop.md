# Daily Operations SOP

## Daily (during the review-queue phase, ~10-15 min)

1. Run/confirm the pipeline executed overnight (GitHub Actions log, or run
   `python -m pipeline.orchestrator --mode daily` manually during setup).
2. Open the review queue (Notion or `data/review_queue/`) — for each pending
   video:
   - Watch it full-through, sound on.
   - Checklist: fact accurate & sourced? Captions synced & typo-free? Visual
     actually matches the claim (no mismatched B-roll)? Tone matches the
     brand (no accidental mocking/sensationalizing)? Watermark present?
     Audio levels balanced (music not drowning narration)?
   - Approve → moves to scheduled publish. Reject → note the reason,
     `pipeline/orchestrator.py` requeues the topic for reproduction rather
     than discarding the researched fact.
3. Spot-check that the previous day's video actually posted correctly on
   both platforms (thumbnail rendering right, no processing error).
4. Skim overnight comments, reply to anything that needs a real answer
   (corrections, questions) — most can be a quick templated reply.

## Weekly (~30-45 min)

1. Pull the week's metrics (views, retention, follower growth, top/bottom
   performing pillar — see docs/07 KPI list).
2. Update `data/facts_database.csv` pillar weighting if one pillar is
   clearly over/underperforming.
3. Top up the facts database — run the topic researcher prompt if the
   `verified`-status queue is running low (keep at least 2-3 weeks of
   verified, unused facts in the queue at all times so a slow week never
   creates a content gap).
4. Publish the week's long-form video (if not already handled by the
   scheduled pipeline) — this is the one asset worth a closer personal
   look given its SEO/search-longevity value (docs/02).
5. Check for any platform policy/API changes that might affect the pipeline
   (YouTube/Meta API changelogs) — low effort, catches breaking changes
   before they silently stop publishing.

## Monthly (~1 hr)

1. Full KPI review against the strategy in docs/02/07 — is the pillar mix
   right, is the cadence right, is it time to move to the next automation
   phase (docs/04) or the next roadmap phase (docs/09)?
2. Refresh the music pool / check for any licensing terms changes.
3. Re-verify a random sample of already-published "verified" facts against
   sources — a lightweight audit trail against drift/complacency in the
   verification process.
4. Review comment sentiment / recurring viewer questions for new content
   ideas — feed directly into the facts database as new `idea`-status rows.

## Incident response (wrong fact published)

1. Correct the video's on-screen text/description immediately if the
   platform allows an edit (YouTube supports description edits; caption/
   video content itself may require a re-upload).
2. Pin a comment or add a community post acknowledging the correction —
   transparency preserves trust better than quietly editing and hoping no
   one notices.
3. Update `data/facts_database.csv`: mark the fact's status/notes with the
   correction and the corrected source, so it can't re-enter the pipeline
   with the same error.
4. If material enough, a short "correcting myself" Short can actually
   perform well and reinforces the channel's credibility — factual channels
   that transparently self-correct tend to build more trust, not less.
