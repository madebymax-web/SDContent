# Legal & Compliance

This is the "things you're probably not thinking about yet" doc. None of this
is legal advice — for anything that touches monetization/business structure,
run it past an actual lawyer/accountant before scaling. This section exists
so the pipeline is built correctly from day one rather than needing a rebuild.

## AI content disclosure (YouTube & Meta)

YouTube's **Altered or Synthetic Content Disclosure Policy** requires
creators to disclose content that is "meaningfully altered or synthetically
generated" when it's realistic enough that a viewer could mistake it for real
footage of a real person, place, or event. Meta has an equivalent AI-label
requirement on Instagram/Facebook.

Practical implications for this pipeline:
- **Real stock footage + TTS voiceover (the default pipeline): the TTS voice
  itself is synthetic, but voiceover narration over real footage is standard
  industry practice and is not what these policies target** — they target
  content that fabricates realistic scenes/events/people. Using AI purely
  for *narration* over real visuals does not require the "altered/synthetic
  content" label. (Using AI to write the script also doesn't trigger it.)
- **If you ever use photorealistic AI-generated video of San Diego places**
  (e.g. Higgsfield/Seedance-class video generation used to fabricate a
  realistic-looking scene), that content likely *does* require disclosure —
  toggle the YouTube "altered or synthetic content" flag on upload, and
  caption/label equivalently on Instagram. This is exactly why docs/04 keeps
  photorealistic AI generation out of the default pipeline — it avoids the
  question entirely for 95%+ of output.
- **Stylized/illustrated AI content** (cartoon, motion-graphics style, used
  sparingly for historical gaps per docs/04) is generally *not* realistic
  enough to trigger disclosure, but label it as an illustration on-screen
  anyway — it's good practice and costs nothing.
- Set a reminder to re-check the current policy text periodically — platform
  AI-disclosure rules are actively evolving; treat this section as a snapshot,
  not a permanent reference.

## Footage & music licensing

- Pexels/Pixabay/Unsplash content used per their respective licenses
  (generally free for commercial use, attribution not required but check
  each platform's current terms — don't assume, verify per API/download).
- Never use footage/photos scraped from Google Images, other creators'
  content, or news outlets without an explicit license — this is the single
  most common copyright strike source for facts/history channels.
- Historical/archival photos: many are public domain (pre-1929 US
  publication, or explicitly released by an institution), but **check each
  archive's specific terms** — a historical society's *digitized copy* of a
  public-domain photo can still carry its own usage restrictions on the scan
  itself. When in doubt, use the institution's officially licensed/press
  materials or credit them on-screen and confirm their sharing policy first.
- Music: royalty-free libraries only (YouTube Audio Library, Pixabay Music,
  or a paid Epidemic Sound/Artlist subscription once revenue justifies it).
  Never a copyrighted commercial track, even a short clip — see docs/03.

## Channel policy setup

- **"Made for Kids" designation**: this content isn't targeted at children,
  so mark the channel/videos as **not made for kids** in YouTube settings —
  gets you comments, end screens, and full monetization features that
  made-for-kids content loses (COPPA restricts these for kids' content).
- **FTC disclosure**: only relevant once/if the channel runs sponsored
  content or affiliate links — not needed at launch, flag for later
  (docs/07 covers monetization triggers).
- **Community Guidelines**: standard factual/educational content is low-risk,
  but keep the "handle with care" categories from docs/05 in mind —
  sensationalized framing of tragedy/disaster content can trigger
  demonetization or content warnings even when factually accurate.

## Platform Terms of Service — automation specifically

- **YouTube Data API**: automated *upload* via API is standard and fully
  supported (that's what the API is for). Automated *engagement* (auto-liking,
  auto-commenting at scale, fake engagement) is against ToS — the publisher
  module only automates upload/scheduling, never engagement manipulation.
- **Instagram Graph API**: requires a Business/Creator account linked to a
  Facebook Page, and the app goes through Meta's standard API review for
  publishing permissions — budget 1-2 weeks for that approval process the
  first time (see docs/09 roadmap).
- Don't run multiple automated accounts that appear to be "faking" organic
  reach (e.g. bot engagement, purchased followers) — both platforms actively
  detect and penalize this, and it would undermine the legitimate growth
  strategy in docs/02.

## Business/tax note

Once this channel earns any revenue (ad revenue, brand deals, affiliate),
that's taxable income — worth a short conversation with whoever handles your
other projects' books about whether it sits under an existing business entity
or needs its own, especially since you've chosen to keep it brand-standalone.
Not urgent at launch; flagging so it's not a surprise later.
