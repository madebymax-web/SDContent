# Content Strategy

## Content pillars

Every fact in `data/facts_database.csv` is tagged with one of these pillars.
Rotating pillars (rather than posting them in blocks) keeps the feed varied and
gives you multiple audience "hooks" instead of one.

1. **History & origin stories** — how a neighborhood got its name, forgotten
   landmarks, "this used to be X," Kumeyaay history, Spanish/Mexican-era San
   Diego, Navy/military history, Balboa Park's 1915 expo origins.
2. **Hidden gems & only-in-SD** — places locals gatekeep, only-in-San-Diego
   quirks (e.g. the Sunny Jim Cave, the Mormon Battalion marker, Spruce Street
   Suspension Bridge), only-here businesses/traditions.
3. **Nature & geography** — microclimates, the county's 70+ miles of coastline,
   canyons within city limits, Torrey Pines being one of the rarest pine species
   on Earth, tidepools, the La Jolla submarine canyon.
4. **Food & drink** — origin of California burritos, craft beer capital history,
   fish taco lore, only-in-SD restaurants that have been around 50+ years.
5. **Weird / surprising facts** — genuinely odd trivia ("did you know") — plane
   crash into a hotel, the Chicken of the Sea/tuna industry history, the world's
   largest outdoor organ (Spreckels Organ), Cabrillo's landing.
6. **Neighborhoods & culture** — what makes each neighborhood distinct (North
   Park, Barrio Logan/Chicano Park, Ocean Beach, Little Italy, Golden Hill),
   murals, local festivals.
7. **"Then vs now" / nostalgia** — archival photo comparisons, what a landmark
   looked like decades ago vs today (strong format for retention — visual
   before/after is an inherent hook).

Target mix once at steady state: roughly even rotation across pillars, biased
slightly toward Hidden Gems and Weird Facts (highest share/save rate in this
category historically) and using History/Then-vs-Now as the long-form anchor.

## Formats

- **Shorts/Reels (primary, daily):** 30-45 sec, single-fact or 3-fact
  "listicle" format, vertical 9:16, captions burned in, hook in first 1.5
  seconds (see hook framework below).
- **Long-form YouTube (weekly):** 6-12 min, either (a) a deep dive on one topic
  ("The Wild History of Coronado's Hotel del Coronado") or (b) a compilation
  ("15 San Diego Facts Even Locals Don't Know"). Compilations are easier to
  batch-produce from the same fact database; deep-dives build more authority
  and rank better in search long-term. Start compilation-heavy, layer in
  deep-dives once the pipeline is proven.
- **Series** (recurring formats, build appointment viewing / recognizability):
  - *"Then vs Now"* — weekly, archival photo vs modern shot of the same spot.
  - *"Wait, That's in San Diego?"* — hidden-gem reveal format.
  - *"60 Second History"* — one historical fact, always same intro card.

## Hook framework (first 1.5 seconds decide everything on Shorts/Reels)

Every script must open with one of these hook patterns — this gets encoded
directly into the script-writing prompt (see `prompts/script_writer_system_prompt.md`):

- **Contradiction/surprise:** "San Diego almost wasn't called San Diego."
- **Visual + question:** "This bridge kills more electricity than a small town —
  here's why." (paired with a striking visual on-screen at frame 1)
- **Local-pride bait:** "If you've never done this in San Diego, are you even
  a local?"
- **Countdown/number:** "3 things under Balboa Park most people never see."
- **Direct claim + payoff withheld:** "San Diego has a bridge that's not
  connected to the mainland by road. Here's how you actually get there."

Avoid generic openers ("Did you know that...") as the *literal first words* —
they're overused and don't stop the scroll. It's fine for "did you know" to be
the *format*, just don't let it be the first four words spoken.

## Platform-specific adaptation

| | YouTube Shorts | Instagram Reels | Long-form YouTube |
|---|---|---|---|
| Length | 30-45s (under 60s) | 30-45s (mirror Shorts cut) | 6-12 min |
| Captions | Burned-in, bold, always on (most watch muted) | Same | Optional but recommended for accessibility |
| Aspect | 9:16 | 9:16 | 16:9 |
| Posting | 1x/day | 1x/day (same asset, IG-native caption/hashtags) | 1x/week |
| Title/caption | Short, curiosity-driven, no clickbait lies | Same + 3-5 relevant hashtags (#SanDiego #SanDiegoLiving #HiddenGems etc.), first comment can carry more hashtags | SEO-optimized title with keyword ("San Diego") near the front, real description with timestamps |
| CTA | "Follow for daily SD facts" | Same, plus occasional "save this for your SD bucket list" (saves are a strong IG ranking signal) | Subscribe + end-screen to related video |
| Cross-post | Same rendered MP4 works for both — no separate edit needed | | Separate 16:9 export from the same source assets |

Repurposing rule: every long-form video should also yield 3-5 short clips (the
most surprising individual facts, re-cut vertical) — this is where Higgsfield's
Shorts Studio restyling tool is genuinely useful (see production pipeline doc),
turning one long-form shoot into a week of shorts.

## Growth strategy

- **Consistency over virality** in month 1-2: the algorithm rewards a channel
  it can predict. Daily shorts, same time of day, same intro/format beat —
  before chasing any individual "viral" swing.
- **Series recognizability**: recurring formats (see Series above) train
  viewers to expect and seek out specific content, which is what turns
  viewers into subscribers/followers on a faceless channel (there's no
  personality to follow, so the *format* has to be the thing people follow).
- **Comment engagement**: faceless channels still need a "someone's home"
  signal — reply to comments (can be templated/batched, doesn't need to be
  real-time), pin a comment asking "which neighborhood should we cover next?"
  to mine future content ideas from the audience itself.
- **Community/local seeding**: early distribution boost from sharing shorts
  into local San Diego subreddits/Facebook groups/Nextdoor *only where
  self-promotion is allowed* — check each community's rules first, and lead
  with the content, not a channel plug.
- **Collabs**: once the channel has a baseline, duet/stitch or cross-promote
  with on-camera San Diego creators — they get faceless-produced factual
  content to react to, you get their audience.
- **SEO compounding**: long-form videos are the asset that keeps working —
  they rank in YouTube/Google search for "san diego [topic]" queries for years.
  Shorts get you discovery velocity now; long-form builds a search-traffic
  moat over time. Don't skip long-form once the pipeline is stable.

## KPIs to watch weekly (see docs/07 for full tracking plan)

- Shorts: average view duration % (retention), not just views — this is the
  single strongest predictor of continued algorithmic distribution.
- Follower/subscriber growth rate week over week.
- Which pillar/format is over-performing — feed that signal back into the
  topic selector's weighting (see `pipeline/topic_selector.py`).
