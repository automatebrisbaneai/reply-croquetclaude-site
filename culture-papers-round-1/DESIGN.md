# DESIGN.md — culture-papers-round-1

A letter from CroquetClaude to Marilyn Nelson, threaded with six questions drawn from how other sports think about culture. Tone is correspondence, not survey. The page should feel like something Marilyn was invited to reply to, not a form she has to fill out.

---

## Remotion hero — 3 concepts

Three options. All are short (6–10 seconds), loop gently, sit in a hero band roughly 680×320 at the top of the page, and share the same restrained palette (off-white page, maroon as single accent, soft paper grain).

### Concept A — "The question, handwritten"

**Motion:** A single line of display serif appears stroke by stroke, left to right, as if written with a nib — `What does winning look like when it's also enjoyable?` — then the ink settles, a faint underline draws itself under one word (`enjoyable`), and the whole line drifts down 4px and steadies. Gentle breath on the underline (opacity 0.9 → 1.0) at the loop point.

**Why it fits:** This is the thesis of the whole correspondence in one line. Marilyn sees the actual question before she scrolls. It tells her "this is a letter, not a survey" faster than any chrome can. Handwriting motion reads as personal without being twee.

**Recommended build:** Remotion with a custom stroke-reveal on SVG `<text>` using `pathLength` and `stroke-dashoffset`. Serif font: Fraunces or Instrument Serif, 600 weight, italic optional on the accented word. One accent colour only (maroon #73182C for the underline, ink-near-black for the glyphs). 8 seconds total — 5s draw, 2s settle, 1s breath before loop.

**Strength:** Highest signal-to-noise. Editorially the strongest of the three.

---

### Concept B — "Clubs drifting into a loose circle"

**Motion:** Six to ten small dots (5–7px, slightly irregular edges like ink spots on paper) enter from different edges of the frame at different speeds. They migrate toward a rough circle — not a perfect one, a hand-traced one. They don't snap: each dot eases into its slot, overshoots by a hair, settles. Then the circle breathes: dots orbit within 2–3px of their resting position, out of phase with each other, so the whole cluster has a living quality. Underneath, in small serif italic, a single line of text fades in: `Twenty-two clubs. One conversation.`

**Why it fits:** The page is about consulting the Golf Croquet community — not Marilyn alone — on what culture wants. The motion literalises that: clubs drifting into something coherent. It's abstract enough to avoid being cute, specific enough to have meaning.

**Recommended build:** Remotion with GSAP-style timeline. Each dot's entry is offset by 0.15s stagger. Dots are SVG circles with a slight filter (feTurbulence at low freq) to suggest ink bleed on paper. Colour: 70% ink-black dots, 30% maroon dots. Resting orbit is a 3px looping sine offset. 10 seconds total.

**Strength:** Most original. Carries the metaphor.

---

### Concept C — "The asterisk writes itself, then the title arrives"

**Motion:** On a blank cream page, a single terracotta asterisk (CroquetClaude's mark) draws itself stroke by stroke — six radial lines from centre outward, each easing in over 120ms with 80ms stagger. Once it's complete, it pulses once (scale 1.0 → 1.04 → 1.0 over 400ms). Then, beneath it, the page title fades up from 0 to 100% opacity over 600ms, offset by 20px: `A letter, in six questions.` Hold for 2 seconds, loop with a 400ms fade-through-white.

**Why it fits:** Simplest. Most CroquetClaude-branded. The asterisk IS CroquetClaude — drawing itself is the character arriving on the page. Works as both identity moment and letterhead.

**Recommended build:** Remotion with staggered stroke draws on an inline SVG asterisk. Each arm is a separate `<line>` with `stroke-dasharray` animation. Maroon asterisk on cream (#FAF9F6). Title in Fraunces 500 italic, ink. 7 seconds total.

**Strength:** Most restrained. Safest bet if Wade wants the hero to feel incidental rather than statement.

---

**Designer's recommendation:** Concept A. It delivers the thesis question at a glance, which is more useful to Marilyn than brand performance (B's metaphor or C's mark). It also makes the whole page feel deliberately editorial rather than utility. Concept B is the most interesting but demands longer motion attention. Concept C is the backup if A's handwriting reveal reads as precious rather than warm in Wade's test.

---

## Page layout direction

**Background:** `#FAF9F6` — warm neutral off-white. Not stark white, not cream. Think a very faint paper warmth. Page bg unchanged top to bottom (no alternating bands, no section dividers with colour).

**Column:** Single column, `max-width: 680px`, centred. No sidebar, no right-rail, no two-column anywhere on the page. At ≥1024px there's generous dead space on either side of the column and the page *breathes*. At <680px the column is 100% width with 24px lateral padding.

**Vertical rhythm:** Generous, non-uniform.
- Remotion hero to CroquetClaude header block: `88px`
- Header block to opener: `48px`
- Opener to first question card: `80px` (big breath — this signals "now the questions begin")
- Question card to next question card: `56px`
- Within a card: preamble → question → buttons: `24px` / `32px` / `24px`
- Last card to submit: `96px`
- Submit to footer: `64px`

Sections feel unhurried. Marilyn should never feel she's being rushed through a form.

**Card anatomy (the 6 question cards):**

Each card uses the MyCroquet pattern:
```
background: #FFFFFF
border: 1px solid #EBE8E1
border-radius: 14px
padding: 32px 36px (desktop) / 24px (mobile)
box-shadow: 0 1px 2px rgba(30, 24, 15, 0.04), 0 4px 14px rgba(30, 24, 15, 0.03)
```

Anatomy top to bottom, inside each card:
1. **Small image** — 64×64px (not huge), slightly offset top-left, no border, sits just above the preamble with 20px margin below. Rounded corners 8px. Subtle desaturation filter (`filter: saturate(0.88) contrast(0.96)`) so the images feel tonal together even when sourced from different photos.
2. **Sports preamble** — 2–4 sentences, serif, 17px, leading 1.65, colour `#4A453D` (soft ink, not black). This is the warmth of the card; it reads like the letter continues.
3. **Thin horizontal rule** — 1px, colour `#EBE8E1`, width 48px (not full width), left-aligned. A small editorial divider marking "now the question comes."
4. **The question** — sans-serif, 18px, weight 500, colour `#1C1916` (near-black with a hint of warmth). Left-aligned. 1.45 leading.
5. **Answer buttons** (MC, see treatment below) or voice textarea. 20px gap between question text and controls.
6. **Voice-enabled textarea** — always present, below buttons if both exist, labelled `Add a thought (or hold the mic)`. See treatment below.

**CroquetClaude header block** (under the hero, above the opener):

```
[avatar 56px]  CroquetClaude
               A letter to Marilyn · Round 1
```

Avatar is the terracotta asterisk, 56×56px, left. Beside it: name in sans-serif 17px weight 600, and a one-line subtitle in sans-serif 14px, colour `#7A7268`, reading `A letter to Marilyn · Round 1`. No border, no box — just two text rows next to the avatar. Horizontal gap `18px`.

**Opener paragraph:**

Serif, 19px, leading 1.7, colour `#2D2822`. Max 4–5 sentences. Addressed explicitly to Marilyn. No blockquote treatment, no drop-cap — just text. This is the letter opening. Left-aligned, not justified.

**Opener tone (from Wade):** Be upfront. The page is asking for Marilyn's croquet context — not delivering insights at her. The opener should say plainly: I've been reading how other sports think about team culture. The research is clear. What I don't have is the croquet picture, and I can't get that anywhere but you. These six questions are me asking.

Draft opener:

> Marilyn — I've spent some time with the research on how other sports build winning team cultures without losing the enjoyment. The patterns are pretty consistent across rugby league, the All Blacks, cycling. What I don't have is the croquet version. I can't get that from a library. These six questions are me trying to get it from you — how you see the cross-club dynamic, what the loudest signals actually are, who's already doing it right. There are no right answers. I just want to know what you know.

**Submit button:**

Single primary button, full column width on mobile, `auto` with `min-width: 280px` on desktop. Filled maroon `#73182C`, white text, 16px weight 500, 12px radius (matches card), padding `16px 28px`, subtle hover lift (translateY -1px, shadow deepens). Label: `Send your reply →`. Centred below the last card with generous space above.

**Footer:**

Small sans-serif, 13px, colour `#9A9389`, centred. One line: `Your answers autosave as you type. Close the page and come back anytime.` Plus a second muted line linking to the privacy note. `48px` below footer before the page ends.

**CroquetClaude identity as accent, not texture:**
- Maroon `#73182C` appears on: submit button, selected MC button state, one underline in the hero if using Concept A, the avatar asterisk
- Lawn green `#82B25E` appears on: active mic state (recording indicator) and nowhere else
- Everything else is neutral tones

No terracotta page background. No cream card backgrounds. The correspondence feeling comes from typography, rhythm, and the serif prose — not from "paper" textures.

---

## Per-question image brief

Each image sits at 64×64px, top-left of its card, rounded 8px, slightly desaturated. All black-and-white or near-monotone preferred so they feel editorial, not photographic.

| Card | Concept | Source to try first | Mood |
|---|---|---|---|
| 1 — Big frame | All Blacks haka formation, or silver fern emblem on jersey | Wikimedia Commons (search "All Blacks haka", "New Zealand rugby union"), fall back to licensed NZ Rugby imagery | Stillness before motion — not the roar, the readiness |
| 2 — Coopetition | Queensland Maroons State of Origin team photo, or Mal Meninga coaching portrait | Wikimedia Commons ("Queensland Maroons", "Mal Meninga"), Pixabay for Australian rugby league | Shoulder-to-shoulder, grit, maroon jersey close-up works too |
| 3 — Loudest artefact | Team selection board (chalkboard with names), or selection announcement moment | Unsplash ("team sheet", "coach whiteboard"), Pixabay for generic dressing-room boards | Analog, handwritten, intimate |
| 4 — Small room | Pat Lam at Connacht Rugby, or any image of a small coaching huddle in a modest venue | Wikimedia Commons ("Pat Lam rugby", "Connacht Rugby"), alternatively a photo of a small regional clubhouse | Underdog dignity — small room, serious faces |
| 5 — Positive deviance | Training session with senior coaching junior, hands-on moment | Unsplash ("coach mentor training", "sports coaching young"), Pixabay for generic training shots — prefer ones that feel lived-in | Transfer of knowledge, concentration, not staged |
| 6 — Open question | No image — or just a 40px asterisk glyph (CroquetClaude's mark, same maroon) in the top-left where an image would go | Use `/apps/reply-croquetclaude-site/assets/drawn-claude.png` scaled down, OR an inline SVG asterisk | "I'm listening" — the card is quieter than the others |

**Sourcing rule:** Wikimedia Commons first (CC-licensed, safe). Unsplash second. Pixabay third. Avoid any image with a visible brand watermark, sponsor logo, or identifiable non-public figure. For the Mal Meninga / Pat Lam cards, if a clear CC-licensed portrait can't be sourced, substitute a generic moment that carries the same mood — the metaphor survives.

**Processing:** Batch-run each image through a subtle desaturation + warm tint in the same pass so all six read as a tonal set. Do NOT convert to ink drawings — that's the retro aesthetic, not this page's aesthetic. Photographic images at low saturation are the right register for the Anthropic/Claude spacious look.

---

## Answer button treatment

Spacious, typographic, restrained. NOT the coloured pill buttons from coaching-list-questions.

**Base state:**
```css
background: #FFFFFF
border: 1px solid #E0DCD3
border-radius: 10px
padding: 14px 20px
font: sans-serif, 15px, weight 500
colour: #2D2822
min-height: 48px (touch target)
cursor: pointer
transition: all 0.18s ease-out
```

**Layout of the button group:**
- On desktop: buttons wrap in a horizontal row, 10px gap between, natural width per button (not equal-width)
- On mobile: buttons stack vertically, full column width, 10px gap between

**Hover:**
- `border-color: #C9C3B6`
- `background: #FAF9F6` (picks up page bg)
- No shadow, no scale. Just a calm surface shift.

**Selected:**
- `background: #73182C`
- `border-color: #73182C`
- `colour: #FFFFFF`
- Font weight stays 500 (no bolding)
- A very subtle inset highlight: `box-shadow: inset 0 1px 0 rgba(255,255,255,0.1)`

**Focus (keyboard):**
- `outline: 2px solid #73182C`
- `outline-offset: 2px`

No icons inside buttons. No leading numbers. No pill shape (radius stays at 10px, matching the card radius family).

If a question has 2–4 options, they sit in one row on desktop. If 5+ options (unlikely), they wrap.

---

## Voice textarea treatment

Always present under each question. Sits below the MC buttons with 24px gap if both exist.

**Container anatomy:**
```
Label (small, above the textarea):
  "Add a thought (or hold the mic to speak)"
  sans-serif, 13px, weight 500, colour #7A7268
  4px margin below

Textarea:
  background: #FAF9F6
  border: 1px solid #EBE8E1
  border-radius: 10px
  padding: 16px 20px (16px right-padding is bumped to 56px to leave room for mic)
  font: serif, 16px, leading 1.55
  colour: #2D2822
  min-height: 96px
  resize: vertical
  transition: border-color 0.18s

  focus:
    border-color: #C9C3B6
    background: #FFFFFF
```

**Mic affordance:**
- Circular button, 36×36px, positioned absolute top-right of the textarea at `top: 12px; right: 12px`
- Base state: transparent background, 1px border `#E0DCD3`, mic icon in `#7A7268`
- Hover: `background: #FAF9F6`, border `#C9C3B6`, icon `#2D2822`
- Active (recording): `background: #82B25E` (lawn green — the ONLY place this green appears on the page), white icon, and a gentle pulsing ring (2px outline animating opacity 0.4 → 0.8 → 0.4 over 1.2s). A small waveform visualiser can appear to the left of the textarea as a 16px-tall bar if feasible.
- Icon: use a clean Lucide `mic` or Heroicons `microphone` — stroke-based, 18px, no fill

The mic is small. It sits quietly top-right. When active it's the only green on the page, which is exactly why it announces itself without shouting.

---

## Typography

**Atkinson Hyperlegible is retained as the base sans-serif** (accessibility non-negotiable for the audience). Paired with a serif for the letter voice.

```css
--font-serif: 'Fraunces', 'Iowan Old Style', 'Georgia', serif;
--font-sans: 'Atkinson Hyperlegible', 'Inter', system-ui, sans-serif;
```

Fraunces is free on Google Fonts, has warm optical sizes, and reads as editorial without being twee (it's the Anthropic-adjacent serif — sibling in spirit to Tiempos and Söhne). Iowan Old Style is the Apple fallback that degrades gracefully.

**Usage map:**
- Opener paragraph, preamble sentences, voice textarea input → **serif** (this is letter prose)
- CroquetClaude header name, question text, button labels, form labels, footer → **sans** (Atkinson, for UI + question clarity)
- Hero Remotion text → **serif** (Fraunces, 500 weight, some italic on accent words)

**Scale:**
```css
--size-hero:    clamp(1.75rem, 3.6vw, 2.25rem);  /* Remotion serif line */
--size-h1:      clamp(1.5rem, 2.8vw, 1.75rem);   /* not used much — this page has no big h1 */
--size-opener:  19px;                             /* opener paragraph */
--size-preamble: 17px;                            /* question preambles */
--size-question: 18px;                            /* the question itself */
--size-body:    16px;                             /* textarea, default sans */
--size-meta:    14px;                             /* header subtitle */
--size-micro:   13px;                             /* textarea label, footer */

--leading-opener: 1.7;
--leading-preamble: 1.65;
--leading-question: 1.45;
--leading-body: 1.55;
```

**Weights:**
- Serif: 400 regular, 500 for the hero and accent moments, italic 400 sparingly (subtitle "Round 1" is italic)
- Sans: 400 regular, 500 for questions / button labels / CroquetClaude name, 600 reserved but mostly unused

Never bold a full paragraph. Never all-caps anything except the mic indicator if needed. Letter-spacing defaults to normal; only the 13px micro labels get `letter-spacing: 0.01em` for legibility.

---

## One distinctive move

**The Remotion hero** (concept A, B, or C depending on Wade's pick) is the single distinctive move. Everything else on the page is restrained by design so the hero has room to land.

- No animated cards, no hover motion on cards, no scroll-driven reveals, no parallax
- No illustrated decorations between cards
- No coloured section dividers
- No icons above headings
- No secondary fonts beyond the serif/sans pair
- No accent colour other than maroon (and the single green mic indicator when active)

The hero animates. The rest of the page sits still and lets Marilyn read.

---

## What this design does NOT have

- ❌ Cream paper backgrounds (that's the old aesthetic — gone)
- ❌ Terracotta as a texture or fill colour on large surfaces
- ❌ Roman numeral chapter markers (editorial cosplay — gone)
- ❌ Pill-shaped coloured answer buttons
- ❌ Rubber-stamp underlines on answers
- ❌ Hand-drawn squiggles or decorative SVGs between sections
- ❌ Drop-caps on the opener
- ❌ Alternating background bands per section
- ❌ A second serif display font layered on the first
- ❌ Full-width card-stretched-to-viewport layouts
- ❌ Icons above each question ("the SaaS-form look")
- ❌ Progress bars across the top ("you're 3/6 through")
- ❌ Centered text anywhere except the submit button and footer
- ❌ Hover scale effects on cards
- ❌ Any motion on cards or text after the hero loop

---

## Mobile adaptations

- Hero Remotion component scales to 100% column width, height reduces to `240px`
- Card padding reduces from `32px 36px` → `24px`
- Card image stays 64×64 but sits inline top-left (not absolute)
- Answer buttons stack vertically at full column width
- Opener font size steps from 19px → 18px
- Voice textarea min-height steps from 96px → 80px
- Submit button goes full width at <720px
- Footer text wraps to 2 lines naturally, stays centred

Nothing gets hidden on mobile. The column just tightens.

---

## Asset dependencies

- `C:\croquet-os\apps\reply-croquetclaude-site\assets\drawn-claude.png` — existing CroquetClaude avatar (used at 56px in the header block and optionally at 40px in Card 6)
- Six sport images (to be sourced per the image brief above, processed to a tonal set, saved into `culture-papers-round-1/assets/`)
- Fonts: Fraunces + Atkinson Hyperlegible via Google Fonts `<link>` (or self-hosted if preferred)
- Remotion component: to be built after Wade picks concept A, B, or C

---

## Done when

- DESIGN.md approved by CroquetClaude and Wade
- Hero concept picked (A, B, or C)
- Six images sourced and processed to tonal set
- HTML/CSS built against this spec
- Accessibility: keyboard nav across all 6 cards, mic button reachable, voice textarea fully operable without mouse, colour contrast ≥ 4.5:1 on all text
- Page breathes at 1440px, holds together at 375px
