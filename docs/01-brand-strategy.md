# Brand Strategy

## Positioning

A faceless, fact-driven channel about San Diego — local history, hidden gems, food,
neighborhoods, only-in-SD oddities, and nature. The presenter is never on camera;
the "host" is a consistent narration voice + visual style, not a person. This is a
deliberate choice: it removes the biggest bottleneck in creator channels (you being
available to film) and lets the channel scale on a content pipeline instead of your
calendar.

Standalone brand for now (per your direction) — no visible tie to your other
projects at launch. Light CTA ("more SD stuff in bio") can be added later once the
channel has traction, without needing a rebrand.

## Channel name options

Criteria used: short, legible at Shorts-thumbnail size, contains "San Diego" or a
strong SD signal for search/SEO, available-sounding as a handle, doesn't collide
with an existing channel (checked via web search — no direct collision found for
any of these as of this writing, but **verify actual handle availability on
YouTube/Instagram/TikTok before you commit**, see checklist below).

| Name | Handle idea | Why it works |
|---|---|---|
| **Finest City Facts** (recommended) | @finestcityfacts | Plays on San Diego's own nickname ("America's Finest City") — locals recognize it instantly, and it reads as a facts-format channel on sight. Strong SEO: contains "facts." |
| SD Unlocked | @sdunlocked | Implies hidden/insider access — good hook for "hidden gems" content. |
| Secret San Diego | @secretsandiego | High search volume pattern ("secret + city" is a proven faceless-channel format), but more generic/crowded category. |
| Only in San Diego | @onlyinsandiego | Clear, welcoming, easy tagline energy ("only in SD..."). Slightly generic pattern used by many "Only in [State]" media brands — check for conflicts with existing "Only In Your State"-style properties. |
| SD Curious | @sdcurious | Playful, implies a running series ("Ever wondered why...") |
| America's Finest Facts | @americasfinestfacts | Longer, but leans fully into the city's identity; good for long-form YouTube title SEO even if the handle is truncated on socials. |

**LOCKED: "Finest City Facts"** (@finestcityfacts). It's ownable (the nickname is
San-Diego-specific, not generic like "Secret" or "Only in"), it's inherently
shareable to locals with civic pride, and "Facts" in the name does real SEO work
on YouTube search and Shorts recommendations.

**Availability check (2026-09-23):** searched YouTube, Instagram, and TikTok for
`@finestcityfacts` — no existing account turned up on any of the three. This
environment's network policy blocks direct requests to instagram.com,
tiktok.com, and youtube.com, so this is a search-index check, not a live
"handle taken" check on each platform's own signup form — **do the final
availability check yourself on each platform's signup screen before you
submit**, since search indexing can miss recently-created or private accounts.

### Registering the handles — this step needs you, not me

Account creation is tied to your personal identity (email/phone verification,
a password only you should set, agreeing to each platform's ToS as yourself),
and this session has no way to complete phone/SMS verification or type a
password on your behalf — nor should it. Here's the exact path for each
platform:

| Platform | Where to register | What it'll ask for |
|---|---|---|
| YouTube | [youtube.com](https://youtube.com) → sign in with/create a Google account → Settings → "Create a channel" → set the handle to `@finestcityfacts` | Google account (email + password), channel name |
| Instagram | [instagram.com/accounts/emailsignup](https://instagram.com/accounts/emailsignup) → sign up → set username to `finestcityfacts` → later: Settings → Account → switch to Professional/Business account (needed for the Graph API publishing in `pipeline/publisher.py`) | Email or phone, password, birthdate |
| TikTok | [tiktok.com/signup](https://tiktok.com/signup) → sign up → Settings → username `finestcityfacts` (defensive registration only, not launching here first per your platform decision) | Email or phone, password |

Once you've registered:
- [ ] YouTube: mark the channel **not made for kids** in Settings → Channel →
      Basic info (see `docs/06-legal-and-compliance.md`)
- [ ] Instagram: convert to a Professional/Creator or Business account and
      link it to a Facebook Page — required before the Graph API can publish
      to it (see `.env.example`'s `IG_*` variables)
- [ ] Send me the channel ID / IG Business Account ID once created and I'll
      drop them into `config/channel_config.yaml` and `.env` for you

### Before you lock it in further
- [ ] Check domain availability if you want a simple link-in-bio page later
      (e.g. finestcityfacts.com).
- [ ] Quick trademark sanity check — "Finest City" is a common San Diego civic
      nickname (not trademarked as far as public record shows), but avoid using
      an actual business's name/slogan.

## Audience

- **Primary:** People with an emotional or practical connection to San Diego —
  current residents, transplants, former residents/alumni, frequent visitors,
  people planning a move or trip. This is a big, evergreen, geographically-anchored
  audience — every US city-facts channel converts on local pride + "I didn't know
  that and I live here."
- **Secondary:** General "interesting facts" / trivia audience who follow
  city-facts and history-facts channels regardless of the specific city (there's a
  proven cross-city format audience: "Did you know..." channels about NYC, LA,
  Chicago, etc. perform well independent of viewer location).
- **Tertiary (long-form only):** Travel planners researching San Diego —
  higher-intent, good for a "12 things to do" or "hidden gems" long-form deep dive
  that ranks in YouTube search for months.

## Tone & voice

- Warm, locally-proud, slightly informal — like a knowledgeable friend, not a
  news anchor or textbook. Short, punchy sentences. Avoid tourism-board stiffness.
- Confident but never smug about "gotcha" facts — the tone is "isn't that cool,"
  not "you're an idiot if you didn't know this."
- Never mocking of San Diego, its neighborhoods, or its people. This is a
  love-letter channel, not a rage-bait or "cities ranked worst to best" channel —
  that distinction is core to the brand and should survive automation (see
  docs/03-style-guide.md for how this gets encoded into the script-writing prompt).

## Visual identity direction

- **Palette:** Sun-bleached coastal — warm sand, Pacific blue/teal, a punch of
  sunset orange/coral as the accent/CTA color. Avoid generic "travel vlog"
  teal-and-orange grade; skew slightly warmer and more editorial (think
  *Sunset Magazine*, not stock-photo travel ad).
- **Typography:** One bold condensed sans for hook/headline text (high
  legibility at thumbnail size), one clean workhorse sans for supporting
  captions. Avoid script/serif fonts — they read slow and hurt Shorts retention.
- **Logo/watermark:** A simple wordmark or a minimal icon (e.g. a stylized wave,
  palm silhouette, or the Coronado Bridge arc) as a small corner watermark on
  every video — cheap, consistent brand recognition without needing a face.
- **Thumbnail style (long-form):** Bold 3-5 word hook text + a striking real
  photo, high contrast, consistent color-graded look across all thumbnails so
  the channel is recognizable in a subscription feed at a glance.

## Competitive landscape (quick scan)

No existing channel is squarely "San Diego facts, faceless, daily shorts" as of
this research pass — the closest analogues are (a) generic multi-city
"facts/secrets" channels that occasionally cover SD, and (b) San Diego-specific
creators who are on-camera lifestyle/vlog channels (see
[15 San Diego YouTubers](https://videos.feedspot.com/san_diego_youtube_channels/)
for the on-camera landscape — useful for competitive/collab research later, not
direct competitors to this format). That's a real opening: city-specific +
faceless + facts is an underserved intersection. Move on it before it isn't.
