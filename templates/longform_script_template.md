# Long-Form Script Template (YouTube, 6-12 min)

Two supported formats — pick per video (see docs/02):

## Format A: Compilation ("15 San Diego Facts Even Locals Don't Know")

```
TITLE: [SEO-forward, keyword "San Diego" near the front]
FORMAT: compilation
TARGET_LENGTH_MIN: [6-10]
FACT_IDS: [ordered list of fact_ids from facts_database.csv, mixed pillars]

--- COLD OPEN (0:00–0:10) ---
VO: [best single fact from the list, teased fast, to hook before the intro card]

--- INTRO CARD (0:10–0:15) ---
[Brand stinger — reused asset, not scripted per video]

--- FACT SEGMENTS (repeat per fact_id, ~30-45s each) ---
SEGMENT N:
  VO: [expanded version of the short-form script for this fact — more detail/context than the Shorts cut]
  ON_SCREEN_TEXT: [section title card, e.g. "#7 — The Cave You Can Walk Into"]
  VISUAL_CUES: [list of 3-5 shots for this segment, more than a Short needs since the segment is longer]

--- OUTRO (last 20-30s) ---
VO: [wrap-up line + subscribe prompt]
END_SCREEN: [suggested next video + subscribe button, standard YouTube end-screen elements]

--- METADATA ---
DESCRIPTION: [keyword-rich, 2-3 sentences + timestamps for each segment + sources listed]
TIMESTAMPS: [0:00 Intro / 0:15 #1 ... — required for YouTube chapters]
TAGS: [SEO tags]
THUMBNAIL_HOOK_TEXT: [3-5 words for the thumbnail]
```

## Format B: Deep Dive ("The Wild History of the Hotel del Coronado")

```
TITLE: [SEO-forward, specific subject named]
FORMAT: deep_dive
TARGET_LENGTH_MIN: [8-12]
SUBJECT_FACT_IDS: [primary fact_id + any related fact_ids that build the narrative]

--- COLD OPEN (0:00–0:15) ---
VO: [most surprising/emotional beat of the story, teased before context]

--- INTRO CARD ---
[Brand stinger]

--- NARRATIVE BEATS (chronological or thematic, not a listicle) ---
BEAT 1: [origin/context]
BEAT 2: [development/turning point]
BEAT 3: [the surprising/payoff detail]
BEAT 4: [where it stands today — ties back to "then vs now" visual pillar if applicable]
  (each beat: VO + ON_SCREEN_TEXT for key facts/dates + VISUAL_CUES)

--- OUTRO ---
VO: [reflective closing line + subscribe prompt]
END_SCREEN: [suggested next video]

--- METADATA ---
[same fields as Format A]
```

Both formats source their per-fact VO content from the same verified rows in
`data/facts_database.csv` as the short-form pipeline — long-form just expands
each with more context/detail rather than requiring new research.
