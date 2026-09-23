# Fact Sourcing & Verification

A facts channel lives or dies on being *right*. One viral "well actually
that's wrong" comment can undo months of trust-building. This process exists
to make errors structurally unlikely, not just to catch them after the fact.

## Sourcing tiers (prefer higher tiers)

1. **Primary/institutional sources** — San Diego History Center, San Diego
   Natural History Museum, Balboa Park Conservancy, City of San Diego official
   records, UC San Diego/SDSU research, National Park Service (Cabrillo
   National Monument), Library of Congress archival records.
2. **Reputable journalism/reference** — San Diego Union-Tribune archives,
   KPBS, Voice of San Diego, well-sourced Wikipedia entries (used as a
   pointer to primary sources, not as the final citation).
3. **Secondary/general reference** — travel guides, general trivia sites,
   other facts channels. **Never use as a sole source** — treat as a lead to
   verify against tier 1/2, not as citable on its own.

Every row in `data/facts_database.csv` has a `source` column — it must point
to a tier 1 or tier 2 source before `verified` is set to `TRUE`.

## Verification process

1. **Claim extraction** — reduce the fact to its precise, checkable claim
   (dates, names, superlatives like "largest/oldest/first" are the most
   common failure points — double-check these specifically).
2. **Cross-check** — confirm against at least one tier-1/2 source
   independent of wherever the fact idea originated. `prompts/
   fact_verification_prompt.md` gives the LLM-assisted first pass; treat its
   output as a draft check, not a final answer — an LLM can be
   confidently wrong about niche local history, so:
3. **Human spot-check** — for anything non-obvious, a superlative claim, or
   anything involving a living person, a specific business, or a sensitive
   event (see "handle with care" below), do a manual check before publish.
   This is the one step in the pipeline that should probably never be fully
   automated away, even after the review-queue phase-out in docs/04.
4. **Phrasing discipline** — when a fact is *likely* true but not fully
   nailed down (contested local legend, folk history), the script must say so
   ("as the story goes...", "local legend has it...") rather than stating it
   as flat fact. This is itself a content angle ("is this SD legend actually
   true?") rather than a liability to hide.

## Handle with care

Flag these categories for extra scrutiny — not off-limits, but they carry
real reputational/legal risk if handled carelessly:

- **Tragedies/deaths** (e.g. the PSA Flight 182 crash, historical
  disasters) — factual, respectful, no sensationalized framing, no dramatized
  reenactment imagery.
- **Living people/current businesses** — verify facts about real, currently
  operating people/businesses especially carefully; avoid anything that
  could read as an unverified claim about a specific person or a negative
  claim about a specific business (defamation risk sits here).
- **Indigenous history (Kumeyaay)** — represent accurately and respectfully;
  prefer sourcing directly tied to Kumeyaay cultural/historical organizations
  where possible rather than only secondhand retellings.
- **Contested/sensitive historical events** (e.g. Japanese American
  internment-era history tied to San Diego, redlining history) — factual and
  respectful, sourced to tier-1 historical records, not flattened into a
  "fun fact" tone mismatched to the subject. Some topics are simply better
  suited to a more measured long-form treatment than a punchy 30-second Short.

## Database status field workflow

`data/facts_database.csv` status values: `idea` → `researching` → `verified`
→ `scripted` → `produced` → `published`. Only `verified` and later can enter
the production pipeline (enforced in `pipeline/topic_selector.py`).
