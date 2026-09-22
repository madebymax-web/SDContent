# Production Pipeline

## Core architecture decision: real footage, not AI-generated scenes

This matters enough to call out before anything else. Two fundamentally
different ways to build "AI B-roll + voiceover" for this channel were
evaluated:

1. **Real stock/licensed footage & photos of actual San Diego** (Pexels/
   Pixabay/Unsplash APIs, plus your own photos/footage over time), assembled
   with Ken Burns motion + TTS voiceover + captions.
2. **Fully AI-generated stylized video** via Higgsfield's `faceless-video`
   workflow (cartoon/claymation/motion-graphics style, 100% synthetic scenes
   in a locked art style — researched directly against the MCP tools available
   in this workspace).

**This framework defaults to option 1 (real footage) as the primary pipeline**,
for three reasons:

- **Authenticity fits the brand.** This is "the city I know and love" — a
  cartoon/AI-animated explainer style is a legitimate faceless format, but it
  reads as generic trivia content, not as San Diego. Real photos/footage of
  actual landmarks is what makes a viewer go "wait, I've been there."
- **Compliance is simpler.** YouTube's Altered/Synthetic Content policy
  requires disclosure for AI-generated content realistic enough to be mistaken
  for real footage of a real place. Real footage sidesteps that question
  entirely; photorealistic AI-generated "San Diego" scenes would need explicit
  per-video disclosure (see docs/06).
- **Cost/scale at daily cadence.** Generating a full video's worth of
  AI video clips per Short (via Seedance/Kling-class models) costs real
  generation credits *every single day*. Sourcing real stock photos/clips is
  free/cheap at this volume and doesn't degrade in quality as you scale output.

**Where Higgsfield genuinely adds value in this pipeline (secondary/optional
roles, not the default engine):**
- **Shorts Studio** (`shorts_studio_create`) — restyle an already-produced
  long-form video into short-form variants. Good for the "one long-form video
  → 3-5 shorts" repurposing workflow in docs/02.
- **`text2speech_v2`** — usable as a TTS fallback with zero extra API-key
  setup, if you don't want to stand up ElevenLabs immediately.
- **Thumbnail/cover generation** and occasional **stylized B-roll for gaps**
  where no real photo exists (e.g., a historical event with no surviving
  photo) — used sparingly, and any such AI-generated shot should be visually
  distinct (illustrated/stylized, not photorealistic) so it's never mistaken
  for real footage, and ideally captioned as an illustration on screen.
- The `faceless-video` cartoon/motion-graphics workflow is a legitimate
  **alternate channel concept** if you ever want a second, purely-animated SD
  channel — flagged here as an option, not built into this pipeline.

## Pipeline overview

```
 1. TOPIC SELECT  →  2. SCRIPT WRITE  →  3. FACT VERIFY (gate)
        │                                        │
        ▼                                        ▼
 data/facts_database.csv            prompts/fact_verification_prompt.md
        │
        ▼
 4. VOICEOVER (TTS)  →  5. SOURCE VISUALS  →  6. ASSEMBLE (ffmpeg)
        │                      │                     │
        ▼                      ▼                     ▼
  ElevenLabs/Higgsfield   Pexels/Pixabay        Ken Burns + cuts +
                          (real SD footage)      color grade + music
                                                        │
                                                        ▼
                                            7. CAPTIONS (Whisper, burn-in)
                                                        │
                                                        ▼
                                            8. THUMBNAIL (long-form only)
                                                        │
                                                        ▼
                                       9. REVIEW QUEUE  (human approve/reject)
                                                        │
                                                        ▼
                                      10. PUBLISH (YouTube + Instagram, scheduled)
                                                        │
                                                        ▼
                                      11. LOG + METRICS PULL (feeds topic_selector)
```

Even though the overall target is **fully automated**, step 9 (review queue)
stays in the loop at launch — see "Automation levels" below for why, and how
it gets removed later without a pipeline rebuild.

## Step-by-step detail

1. **Topic select** (`pipeline/topic_selector.py`): pulls the next unused,
   verified fact from `data/facts_database.csv`, weighted by pillar rotation
   and recent performance data (once metrics exist). Falls back to an
   LLM-assisted research step (`prompts/topic_researcher_prompt.md`) when the
   queue of pre-verified facts runs low — but *researched* facts always route
   through step 3 before they're usable.
2. **Script write** (`pipeline/script_writer.py`): calls the Anthropic API
   with `prompts/script_writer_system_prompt.md` (encodes hook framework,
   tone rules, word-budget-per-duration from docs/02-03) to produce a
   timed script: hook line, body beats, on-screen text cues, and a visual
   shot list (what real-world subject each beat needs, for step 5).
3. **Fact verification gate**: any fact not already marked `verified=TRUE`
   in the database must pass a verification pass (LLM-assisted source check
   + your own spot-check for anything non-obvious) before it can proceed.
   See docs/05 for the full process. This is a hard gate, not a suggestion —
   publishing a wrong "fact" is the single fastest way to lose trust in a
   facts channel.
4. **Voiceover** (`pipeline/tts.py`): renders the script's spoken lines via
   ElevenLabs (or Higgsfield `text2speech_v2` fallback) using the locked
   channel voice ID from `config/channel_config.yaml`.
5. **Source visuals** (`pipeline/visuals.py`): pulls real photos/video clips
   matching the shot list from Pexels/Pixabay (San Diego-specific search
   terms per beat), caches to `assets/cache/`, flags any beat that has no
   good real-footage match for manual sourcing or (sparingly) an illustrated
   Higgsfield asset.
6. **Assemble** (`pipeline/assembler.py`): ffmpeg pipeline — Ken Burns
   motion on stills, hard cuts on voiceover beat timing, color grade LUT,
   ducked music bed, watermark overlay. Outputs a clean (caption-free) master
   render first, per the style guide's word on captions needing word-level
   timing from the *clean* voice track.
7. **Captions** (`pipeline/captioner.py`): faster-whisper transcribes the
   clean voice track for word-level timestamps, burns styled captions per
   docs/03, outputs the final render.
8. **Thumbnail** (`pipeline/thumbnail.py`, long-form only): composites hook
   text over a selected frame/photo per the thumbnail style guide.
9. **Review queue**: final render + proposed title/description/hashtags land
   in a review folder (or Notion database, see below) for a quick approve/
   reject pass before anything goes out.
10. **Publish** (`pipeline/publisher.py`): YouTube Data API v3 upload
    (scheduled publish time), Instagram Graph API publish (requires the
    render to be at a public URL first — see `.env.example` MEDIA_HOST_*).
11. **Log + metrics**: run outcome and (once available) platform analytics
    get written back to the facts database / a metrics log, which feeds the
    topic selector's pillar-weighting over time.

## Automation levels (how "fully automated" gets phased in safely)

You asked for fully automated end-to-end — that's the target, and the
pipeline is built to run unattended. The one deliberate speed bump is the
step 9 review queue, and it's there for a concrete reason: a factual-content
channel's entire value proposition is trust, and the failure mode of *zero*
human review (a wrong fact, a bad AI mispronunciation, a caption typo, a
visual that doesn't match the claim) is expensive to reputation in a way
that's disproportionate to the few minutes a review costs. Recommended
phase-out:

- **Weeks 1-4:** every video reviewed before publish (5-10 min/day).
- **Weeks 5-8:** spot-check review — auto-publish, but a daily digest lets you
  pull anything back within a delay window (e.g. schedule publish 2 hours
  after render, review in that window).
- **Week 9+:** if the verification gate + spot-checks haven't caught real
  errors, remove the human gate entirely and let `orchestrator.py` run fully
  unattended on the GitHub Actions schedule.

This is a config flag (`review_required` in `config/channel_config.yaml`),
not a code change — flip it when you're ready.

## Tool stack summary

| Stage | Primary tool | Notes |
|---|---|---|
| Script generation | Claude API (Anthropic) | Already have access via this environment's credentials pattern |
| Voiceover | ElevenLabs | Higgsfield `text2speech_v2` as zero-setup fallback |
| Visuals | Pexels/Pixabay APIs | Free tier sufficient at this volume; real footage |
| Assembly | ffmpeg (via `ffmpeg-python`) | Runs anywhere, no per-render cost |
| Captions | faster-whisper (local) | No API cost, runs on CPU |
| Thumbnails | Pillow / Adobe Express (already available in this workspace) | Adobe's design tools are a strong option for polished thumbnail templates |
| Content calendar / review queue | Notion (already connected) or flat files in `data/` | Notion recommended once you're reviewing daily — better UX than CSVs |
| Publishing | YouTube Data API v3, Instagram Graph API | Requires app registration/OAuth — see docs/09 roadmap for setup order |
| Scheduling/orchestration | GitHub Actions cron (`.github/workflows/daily-content.yml`) | Fully automated, runs in this repo |
| Optional restyling/repurposing | Higgsfield Shorts Studio | Long-form → shorts repurposing pass |

See `pipeline/` for the actual code scaffolding implementing each stage.
