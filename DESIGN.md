# DESIGN.md — reply.croquetclaude.com

## Creative concept (one sentence)

A handwritten letter from CroquetClaude to the recipient, with the coach questions threaded inline as marginal queries — an editorial essay that happens to collect answers, not a form that happens to have voice.

## Why this fits (classy + easy to read + CroquetClaude)

- **Classy** — editorial serif typography, generous whitespace, single continuous column reading like a Marginalian or Kinfolk essay page. No SaaS cards, no pill buttons, no badge stamps.
- **Easy to read** — body stays Atkinson Hyperlegible ≥ 18px, line-height 1.78, single-column reading rhythm (no side-by-side grids to track). Section markers are large roman numerals so Marilyn can find where she was mid-session.
- **CroquetClaude** — terracotta asterisk mustache is a writer's portrait at the top, not a mascot. Hand-drawn energy lives in typography choices (display serif, marginal annotations, rubber-stamp answer marks), not in illustrated decoration piled on top of the layout.

## Reference sites

- **The Marginalian (themarginalian.org)** — warm cream background, serif display pulling weight for hierarchy, inline author portraits, unhurried leading. Generous whitespace between thoughts.
- **Kinfolk article pages** — editorial restraint, the display serif as THE distinctive move, body copy treated as reading material not UI.
- **Old letterpress correspondence** — rubber-stamp marks (INCLUDE / DROP / UNSURE) set off with all-caps tight tracking and ink-red underlines, not pill shapes.

## Layout pattern

Single-column reading layout, max-width ~680px on desktop (narrower than form-wide to enforce reading-column rhythm). Center-aligned container, left-aligned text throughout. No grid. No cards. Coach entries are typeset paragraphs with inline answer marks below.

Section markers: large Roman numeral (I / II / III) in display serif, flanking the section title. Chapter-opener feel.

## Colour palette (kept from brand, refined roles)

```css
--ink: #1f2421;              /* primary text — letterpress black-green */
--ink-soft: #3d4843;         /* secondary prose */
--ink-faint: #707a73;        /* meta details (club, ACA#) */

--paper: #fdf7e4;            /* main page — aged cream writing paper */
--paper-deep: #f6ecc7;       /* rule lines, soft accents */
--paper-edge: #e8dba8;       /* hairline dividers, inline separators */

--lawn: #2d6a4f;             /* kept — CroquetClaude primary */
--lawn-deep: #122d22;        /* letterhead bar only */
--lawn-ink: #1b4332;         /* section roman numerals */

--terracotta: #bc6c25;       /* CroquetClaude avatar — used sparingly for accents */
--terracotta-ink: #8e4f17;   /* hover/pressed on terracotta marks */

--stamp-drop: #9e2a1e;       /* drop answer — deep ink red, not alert red */
--stamp-include: #2d6a4f;    /* include — lawn */
--stamp-unsure: #8e4f17;     /* unsure — terracotta ink */
```

## Typography scale

**Display serif:** `Cormorant Garamond` weights 500/600, italic — free on Google Fonts. Used for: H1, section titles ("I. Active in RevSport…"), roman numeral markers, thank-you headline, opener first-words drop-accent.

**Body:** `Atkinson Hyperlegible` 400/700 regular + italic — kept for accessibility. Used for: all prose, coach names, answer marks, meta data, buttons, notes.

```
--font-display: 'Cormorant Garamond', 'Georgia', 'Times New Roman', serif;
--font-body: 'Atkinson Hyperlegible', 'Segoe UI', sans-serif;

--size-opener: clamp(1.2rem, 2.2vw, 1.35rem);   /* 19–22px */
--size-body:   clamp(1.05rem, 1.4vw, 1.125rem);  /* 17–18px — bumped ≥17 */
--size-meta:   0.9rem;                            /* 14.4px */
--size-stamp:  0.78rem;                           /* rubber-stamp label */

--h1: clamp(2.2rem, 5vw, 3.2rem);                /* serif display */
--h2: clamp(1.6rem, 3.2vw, 2.1rem);              /* serif section */
--numeral: clamp(3.2rem, 7vw, 4.8rem);           /* roman numeral */

--leading-body: 1.78;
--leading-opener: 1.62;
--leading-display: 1.08;
```

## Components

### Letterhead (kept, refined)
Dark lawn bar with CroquetClaude wordmark left, mission title right. Wordmark switches to display serif italic weight — subtle but shifts register from corporate to editorial. Bottom dotted seam kept.

### Opener — "letter beginning" treatment
- Drawn CroquetClaude portrait (~120px square, no clip, no border, hand-drawn lives free on the paper) floats LEFT of the opening paragraph on desktop, above on mobile
- First three words "Hi Marilyn —" set in display serif italic, 1.2× size, as drop-in
- Body prose in body font, 1.2rem, line-height 1.62
- No blockquote bar, no box

### Section chapter-openers (replaces "Section A" pill)
```
I.    Active in RevSport but missing
      from your February list (5)
      ─────────────────────────────
```
- Large roman numeral in display serif, lawn-ink, set flush left with hanging indent
- Title beside it in display serif, 500 weight
- Count in italic secondary
- Horizontal hairline rule with paper-edge tone — thin, restrained
- Subtitle in body italic, grey, below

### Coach entry (replaces card)
NOT a card. A typeset paragraph-block:
```
Lenton, Jill
Bribie Island · Golf 1 · ACA 43913

    [ include ]   [ drop ]   [ unsure — tell me more ]
```
- Name in body 700, 1.15rem, followed by META inline-separated with bullet
- Meta in ink-faint, small caps, letter-spaced, minimal
- Three answer marks in a row, 1.25rem padding above, left-aligned
- No card background. No border. Vertical spacing (2rem gap between coaches) does the separation work.
- Hairline between entries? Only if it survives visual test — prefer whitespace-only separation.
- **Answered state:** the chosen mark gets a small hand-drawn underline (inline SVG squiggle), chosen-colour ink, rest of marks fade to 45% opacity
- **Missing state (validation):** small left-rule in stamp-drop red, no scary red outline

### Answer marks (replaces pill buttons)
Rubber-stamp style:
- Small caps, letter-spacing 0.12em, weight 700
- Body font (not display — kept readable)
- `underline-offset: 0.25em` with a 2px underline in the answer's accent colour
- Horizontal padding 0.2rem, no background by default
- Hover: paper-deep wash + underline thickens
- Selected: accent-colour wash behind + darker ink + persistent underline

Labels stay short and direct: `include` / `drop` / `unsure —` or `include ✓ aca on file` etc.

### Roman-numeral background mark
Giant faint roman numeral sits in the left margin of its section on desktop (right-aligned in a margin column), cream-on-cream, opacity 0.04. Editorial-magazine chapter-opener tactic. Hidden below 900px width.

### General notes textarea
Still a textarea, but restyled: no rectangular card, labelled "P.S. — anything else I should know?" in display serif italic, textarea has paper-deep wash background, no hard border, just a faint underline rule.

### Submit
`Send my letter →` — body font, all-lowercase italic weight NOT used (keeps it readable for the target age group), plain ink with right-arrow. Letterpress feel via paper-edge underline that thickens on hover. Not a button shape — a signature-line gesture.

### Thank-you screen
Party-CroquetClaude (~180px) at top-centre. Display-serif headline "Thanks, Marilyn." then body paragraph. One sentence — "Wade will see your answers right away." Minimal whitespace.

## Paper texture

Kept: repeating faint rule-lines and soft warm wash. Added: very subtle paper grain via SVG noise filter at 0.03 opacity so the page breathes as paper does. Not aggressive.

## What this design does NOT have

- ❌ No card containers with shadow + rounded corners (the "nicer form" vibe)
- ❌ No green/red/amber pill buttons
- ❌ No numbered badge stamps on each card
- ❌ No dotted-rule section dividers (replaced with a single editorial hairline)
- ❌ No centred hero text or hero image
- ❌ No SaaS palette accents
- ❌ No icon above each heading
- ❌ No em-dash separators (AI tell) in copy — em-dashes allowed in display but rare
- ❌ No identical padding throughout sections
- ❌ No repetitive symmetrical grid

## Mobile adaptations

- Portrait stacks above opener (not beside)
- Roman numerals reduce in size, stay inline with title
- Answer marks wrap to 2 rows if needed (3 marks → 2 rows at ≤400px)
- Margin-column background numerals hidden
- Body stays 17px minimum
