# Short-Form Script Template (Shorts / Reels, 30-45s)

Fill every bracketed field. This is the structure `pipeline/script_writer.py`
asks the LLM to produce as JSON (see `prompts/script_writer_system_prompt.md`) —
this markdown version is the human-readable reference/example.

```
TITLE (on-screen, YouTube metadata): [5-8 words, curiosity-driven, no clickbait lies]
FACT_ID: [row id from data/facts_database.csv]
PILLAR: [history | nature | hidden-gems | food | weird | neighborhoods | then-vs-now]
TARGET_LENGTH_SEC: [30-45]

--- HOOK (0:00–0:02) ---
VO: [1 punchy line, contradiction/question/local-pride/countdown pattern — see docs/02]
ON_SCREEN_TEXT: [same line or tighter, must be legible instantly]
VISUAL_CUE: [what real-world subject/shot this needs — e.g. "wide shot, Coronado Bridge, golden hour"]

--- BODY BEAT 1 (0:02–0:0X) ---
VO: [one clear idea, ~15-20 words]
ON_SCREEN_TEXT: [key phrase or number, not full VO text]
VISUAL_CUE: [specific real photo/footage subject]

--- BODY BEAT 2 (...) ---
VO: [...]
ON_SCREEN_TEXT: [...]
VISUAL_CUE: [...]

--- PAYOFF / BUTTON (last 2-4s) ---
VO: [the "so what" — why this matters/lands emotionally, or a final surprising beat]
ON_SCREEN_TEXT: [...]
VISUAL_CUE: [...]

--- CTA CARD (final ~1s, reusable brand asset, not per-script) ---
"Follow for daily San Diego facts"

--- METADATA ---
CAPTION: [platform caption, 1-2 sentences + 3-5 hashtags for IG]
HASHTAGS: [#SanDiego #SanDiegoLiving #HiddenGems ... pillar-specific tags]
SOURCE_CITATION: [pulled from facts_database.csv `source` column — kept internally, not shown on screen unless the claim needs an on-screen citation per docs/05]
```

## Example (fact_id 14 — Sunny Jim Cave)

```
TITLE: The Cave You Can Actually Walk Into in La Jolla
FACT_ID: 14
PILLAR: hidden-gems
TARGET_LENGTH_SEC: 32

--- HOOK (0:00–0:02) ---
VO: "There's a sea cave in La Jolla you don't need a boat to get into."
ON_SCREEN_TEXT: "You don't need a boat for this cave."
VISUAL_CUE: La Jolla coastline, sea caves visible from cliff, wide establishing shot

--- BODY BEAT 1 ---
VO: "It's called Sunny Jim Cave — and there's a tunnel dug straight down into it."
ON_SCREEN_TEXT: "Sunny Jim Cave"
VISUAL_CUE: Entrance to the tunnel/shop above the cave

--- BODY BEAT 2 ---
VO: "It was hand-dug back in 1903, and yes — it was actually used for smuggling."
ON_SCREEN_TEXT: "Dug in 1903"
VISUAL_CUE: Interior tunnel shot / stairs descending

--- PAYOFF ---
VO: "It's the only sea cave in California you can walk straight down into."
ON_SCREEN_TEXT: "Only one like it in CA"
VISUAL_CUE: View out from inside the cave toward the ocean

--- CTA CARD ---
"Follow for daily San Diego facts"

--- METADATA ---
CAPTION: "You've probably driven past this a hundred times. 🌊 #SanDiego #LaJolla #HiddenGems"
HASHTAGS: #SanDiego #LaJolla #HiddenGems #SanDiegoLiving #CaliforniaCoast
SOURCE_CITATION: Cave Store La Jolla / San Diego History Center
```
