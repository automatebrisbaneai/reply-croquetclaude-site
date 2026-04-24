# DESIGN.md — news-site-design-pick-2026-04

**Mission:** News site design pick, April 2026
**Recipient:** Wade Hart (internal)
**Built by:** Reply Builder Claude
**Date:** 2026-04-24

---

## Visual direction

Spacious layout, clean whites, warm cream page background (`#f8f5ee`).
CroquetClaude avatar top-left in site header (drawn-claude.png, 36px tall).
Atkinson Hyperlegible body font, 17px+, line-height 1.65.

Page background: warm off-white `#f8f5ee`
Cards: white `#ffffff` with `1px solid #e8e2d6` border, 10px border-radius
Opener: cream `#fefae0` callout with 4px left border in lawn green `#2d6a4f`

---

## Section structure

**Section A — Pick the look (7 cards)**
- Each card: 180px thumbnail column + body text column
- Body: theme name, vibe sentence, trade-off sentence (prefixed "Trade-off:" in terracotta)
- Links: "Open demo ↗" and "Repo ↗" in small lawn-green underline text
- Footer zone: Pick (lawn green) / Skip (terracotta) buttons + notes textarea (opens on any answer)

**Section B — Stack direction (1 card)**
- Three custom answer buttons: Keep Next.js / Swap to Astro (both green) + Whatever fits the theme (terracotta)
- Notes textarea opens on any answer

**Section C — From the old prototype (5 cards)**
- Keep (green) / Drop (red `#b83227`) / Unsure (terracotta) buttons
- Notes textarea opens on Unsure

---

## Images

All thumbnails: 400x250 PNG, captured via Playwright at desktop 1200x800.
Stored at `images/` within the mission directory.

Files: source.png, casper.png, dope.png, ruby.png, tailwind-nextjs.png, fuwari.png, custom.png

---

## Thank-you screen

Text: "Thanks Wade. I'll pull the theme apart and come back with a rebuild plan."
(Rendered by app.js shared submit handler.)
