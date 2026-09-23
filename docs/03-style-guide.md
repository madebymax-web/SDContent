# Style Guide

## Visual style

- **Footage source:** Real photo/video of actual San Diego places is the
  default (see docs/04 for why — briefly: authenticity and disclosure-policy
  reasons). Ken Burns-style slow pan/zoom on high-res stills, cut on the beat
  of the voiceover every 2-4 seconds to hold attention.
- **Color grade:** Warm, slightly lifted shadows, punchy but not oversaturated
  blues (ocean/sky) — consistent LUT/preset applied in the assembly step so
  every video looks like it belongs to the same channel even though source
  footage varies in origin/quality.
- **Motion:** Subtle zoom/pan only — no spinning/glitch transitions by default
  (reads as low-effort meme content, undercuts the "trustworthy facts" brand).
  Hard cuts between shots, no crossfades (crossfades read slow on Shorts).
- **On-screen text:** Every spoken hook line is echoed as bold on-screen text
  in the first second — critical since most viewers start muted. Supporting
  facts get lighter-weight caption styling (see Captions below).
- **Watermark:** Small corner logo/wordmark, low opacity, present on every
  video (brand recognition + reduces reposting-without-credit).

## Captions

- Burned-in, word-by-word or short-phrase reveal timed to speech (via Whisper
  word-level timestamps — see `pipeline/captioner.py`).
- Bold condensed sans, high-contrast (white text, dark outline/shadow — must
  read over any background), centered lower-third or center-safe zone
  (avoid the very bottom third where platform UI overlaps on Shorts/Reels).
- Emphasize the single most important word per line with a color accent
  (the sunset-orange brand accent) — proven retention technique, used
  sparingly (not every word) so it doesn't lose meaning.

## Voice / narration

- **Provider:** ElevenLabs by default (best-in-class prosody for factual/
  documentary narration); Higgsfield's `text2speech_v2` is available as a
  zero-setup fallback already in this workspace.
- **Voice character:** Warm, mid-register, conversational-documentary — think
  a knowledgeable friend telling you something cool, not a movie-trailer
  announcer and not a monotone textbook reader. Avoid overly "hype" energetic
  voices — mismatches the trustworthy/local-pride tone.
- **Consistency:** Lock one voice_id for the life of the channel (voice
  consistency is itself a brand asset — viewers recognize it). Store the
  chosen ID in `config/channel_config.yaml`, never hardcode in scripts.
- **Pacing:** ~150 words/minute target for Shorts (fast enough to fit a full
  fact in 30-45s, slow enough to stay intelligible) — the script writer prompt
  enforces a word budget per video length (see `prompts/script_writer_system_prompt.md`).

## Music

- Low, unobtrusive bed underneath narration — should never compete with
  voice or captions for attention. Duck (auto-lower) music volume under
  narration in the assembly step.
- Source from royalty-free/licensed libraries only — YouTube Audio Library,
  Epidemic Sound (if subscribed), or Pixabay Music. Never use commercially
  copyrighted music, even short clips — copyright claims can mute audio or
  block monetization retroactively across the whole catalog on some platforms.
- Keep a small rotating pool (8-12 tracks) rather than one loop, tagged by
  mood (upbeat/curious vs reflective/historical) matched to pillar in
  `config/channel_config.yaml`.

## Thumbnails (long-form)

- Bold 3-5 word hook text, one strong real photo, consistent color treatment
  matching the video color grade.
- Face-free by definition — lean on the photo subject + text hierarchy
  instead of a reaction-face thumbnail (the usual YouTube CTR trick, not
  available here — compensate with stronger text hooks and a genuinely
  striking/unusual photo choice).

## Intro / outro

- No long intro — cold open on the hook within the first second, always.
  A locked 0.5s brand stinger (logo + sound) is fine as a *transition*
  element between the hook and the body, not as a delay before it.
- Outro: brief, consistent CTA card ("Follow for daily San Diego facts") —
  under 2 seconds on Shorts, slightly longer end-screen with subscribe
  prompt + suggested next video on long-form.

## What this style guide deliberately avoids

- No mocking/negative "worst of" framing (brand rule from docs/01).
- No jump-scare/loud sound-effect gimmicks — undercuts trust in a facts
  channel.
- No AI-generated "photorealistic" imagery of real San Diego places/people
  presented as if real — see docs/06 legal/compliance for why this is a hard
  rule, not just a style preference.
