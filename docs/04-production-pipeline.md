# Production Pipeline

## Core architecture (revised): Higgsfield-driven, zero external API keys

**Superseded 2026-10-05.** The original version of this doc defaulted to
real stock footage (Pexels) + ElevenLabs TTS + a standalone Python/ffmpeg
pipeline, specifically to avoid AI-content-disclosure questions and the cost
of daily AI video generation. That tradeoff changed once we accounted for
what's actually sitting in this environment: a connected **Higgsfield**
account (Plus plan, credits already available) whose `faceless-video`
workflow does script → style-locked visuals → locked-voice narration →
assembled, captioned video **end to end in one workflow**, callable directly
from a Claude Code session with no separate API key, billing account, or
standalone script required.

The decision: **go full Higgsfield.** No Anthropic API key (script writing
happens in-session), no ElevenLabs key (Higgsfield `text2speech_v2` handles
narration), no Pexels key (Higgsfield generates the visuals too). The
tradeoff this reopens — and how it's handled:

- **Authenticity**: Higgsfield's `faceless-video` workflow renders a
  **stylized, non-photorealistic** look (motion graphics, watercolor,
  papercraft, flat vector, etc. — not attempted photoreal footage of real
  places). That's a deliberate choice, not a limitation: it keeps the
  channel out of AI-disclosure territory (see below) and it's a legitimate,
  common "explainer" aesthetic for a facts channel. **Default style preset:
  "Editorial Motion Graphics"** — clean, editorial, reads as credible/
  informational rather than cartoonish, closest fit to the "knowledgeable
  friend" tone in docs/03. Never select a photorealistic-leaning preset for
  real San Diego landmarks — that's the one thing that would trigger the
  disclosure question below.
- **AI content disclosure**: per docs/06, YouTube/Meta's disclosure
  requirement targets content realistic enough to be mistaken for real
  footage of a real place/person/event. A stylized motion-graphics/
  illustrated look does not read as real footage, so it falls outside that
  requirement — confirmed by sticking to non-photorealistic presets only.
- **Cost**: this runs on your existing Higgsfield credits, not a new
  per-API-call bill. At ~320 credits available on the Plus plan, check
  actual per-video credit cost (`mcp__Higgsfield__ads_studio_quote`-style
  pre-flight check, or just watch the balance after the first few runs)
  before committing to a daily cadence — if credits run tight, the Plus
  plan's refill/top-up is the lever, not a second provider.

The original real-footage + Python/ffmpeg pipeline (`pipeline/*.py`,
`.github/workflows/daily-content.yml`) is kept in the repo as an **alternate,
self-hosted path** — useful if you ever want this to run completely outside
Claude Code (e.g. on your own server, with your own API keys, no Higgsfield
dependency). It is no longer the primary path. See "Alternate path" at the
bottom of this doc.

## Pipeline overview (primary path: Claude Code Routine + Higgsfield)

```
 1. TOPIC SELECT  →  2. FACT VERIFY (gate)  →  3. HIGGSFIELD faceless-video
        │                      │                         │
        ▼                      ▼           (script + style-locked visuals +
 data/facts_database.csv  prompts/fact_        text2speech_v2 narration +
                           verification_          assembly + captions, one
                           prompt.md               workflow call)
                                                         │
                                                         ▼
                                              4. REVIEW QUEUE (human approve/reject)
                                                         │
                                                         ▼
                                              5. PUBLISH (YouTube + Instagram)
                                                         │
                                                         ▼
                                              6. LOG + METRICS (feeds topic_selector)
```

A daily **Claude Code Routine** (a scheduled trigger that fires a prompt
into a session, see `mcp__Claude_Code_Remote__create_trigger`) drives this:
it wakes up, reads `data/facts_database.csv`, picks the next eligible fact,
runs the verification gate if needed, calls the `faceless-video` workflow
with the locked style preset and voice, and drops the result in the review
queue (or publishes directly once `review_required` is turned off).

## Step-by-step detail

1. **Topic select**: the Routine's prompt instructs Claude to read
   `data/facts_database.csv`, filter to `status=verified`, and pick the next
   one per the pillar weighting in `config/channel_config.yaml` — this is
   the same selection logic as `pipeline/topic_selector.py`, just run by the
   agent directly instead of imported as a Python module.
2. **Fact verification gate**: unchanged from the original design — any
   fact not already `verified` gets checked against
   `prompts/fact_verification_prompt.md` before it can be produced. Still a
   hard gate (see docs/05).
3. **Generate** (one Higgsfield `faceless-video` workflow call): channel
   type **Explainer**, mode **Animated**, style preset **Editorial Motion
   Graphics** (locked in `config/channel_config.yaml`), topic = the
   selected fact's text, voice = a locked `text2speech_v2` voice_id. The
   workflow internally handles script beats, a consistent style-locked
   asset roster, 10-second video blocks, narration, ffmpeg assembly, and
   burned-in captions — see `get_workflow_instructions(workflow="faceless-video")`
   for the full internal recipe if you need to debug a specific stage.
4. **Review queue**: the finished video + proposed title/caption/hashtags
   land in a review folder (or Notion, see docs/04's tool stack) for a
   quick approve/reject pass — same role as before, see "Automation
   levels" below for the phase-out plan.
5. **Publish**: YouTube Data API v3 + Instagram Graph API, same as the
   original design (`pipeline/publisher.py`'s logic still applies — it's
   just invoked by the Routine/agent rather than a cron'd Python script).
   This is the one stage that still needs real external credentials
   (OAuth), because publishing to your own YouTube/Instagram accounts isn't
   something Higgsfield or this session can shortcut — see docs/09.
6. **Log + metrics**: publish outcome and (once available) platform
   analytics get written back to the facts database, feeding pillar
   weighting over time — same as the original design.

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
  errors, remove the human gate entirely and let the Routine publish
  directly after generation.

This is a config flag (`review_required` in `config/channel_config.yaml`),
not a code change — flip it when you're ready.

## Tool stack summary (primary path)

| Stage | Primary tool | Notes |
|---|---|---|
| Script + visuals + voice + assembly + captions | Higgsfield `faceless-video` workflow | One workflow call; Editorial Motion Graphics preset, locked voice_id — no external API key |
| Orchestration | Claude Code Routine (scheduled trigger) | Fires a prompt daily; the agent does topic selection, verification, and the workflow call in-session |
| Content calendar / review queue | Notion (already connected) or flat files in `data/` | Notion recommended once you're reviewing daily — better UX than CSVs |
| Thumbnails | Higgsfield (same workflow's thumbnail step) or Adobe Express | Adobe's design tools are a strong option if you want a distinct thumbnail template |
| Publishing | YouTube Data API v3, Instagram Graph API | Still requires app registration/OAuth — the one stage with real external credentials, see docs/09 |
| Optional restyling/repurposing | Higgsfield Shorts Studio | Long-form → shorts repurposing pass |

## Alternate path: standalone Python/ffmpeg pipeline (no Claude Code dependency)

The repo still contains a complete, working alternative in `pipeline/*.py`
(`topic_selector.py`, `script_writer.py`, `tts.py`, `visuals.py`,
`assembler.py`, `captioner.py`, `thumbnail.py`, `publisher.py`,
`orchestrator.py`) plus `.github/workflows/daily-content.yml`. This path
needs its own API keys (Anthropic, ElevenLabs, Pexels — see
`.env.example`) and runs as a plain script, independent of any Claude
session. It's not the recommended path anymore, but it's worth keeping if
you ever want this running somewhere that isn't Claude Code, or want
real-footage visuals instead of Higgsfield's stylized look — both designs
read from the same `data/facts_database.csv` and `config/channel_config.yaml`,
so switching later doesn't mean starting over.
