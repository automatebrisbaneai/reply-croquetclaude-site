# DESIGN.md — mockup-feedback-template

**Mission:** Mockup-feedback rounds (CAQ public site + news.croquetqld.org)
**Built by:** CroquetClaude
**Date:** 2026-05-07
**Status:** Template scaffold — Phase 0.1 of `boards/mockup-feedback-rounds.md`. Phase 3.1/3.2 fork this into per-surface mission directories.

---

## Purpose

Reusable structure for "rank these three variants of the same surface" stakeholder asks. Drives Phase 3 of the mockup-feedback-rounds project. Forks twice: once for CAQ public site, once for news.croquetqld.org. Each fork swaps the seed file (variant names, taglines, deploy URLs, thumbnails) and gets minted per-stakeholder tokens.

## Visual direction

Same chrome and palette as `news-site-design-pick-2026-04` — Chrome A standard site-header, warm cream `#f8f5ee` page bg, white cards, Atkinson Hyperlegible body. CAQ palette accents (lawn green, terracotta) flag rank state.

## Section structure

### Opener
Cream callout, 4px lawn-green left border. Surface-specific copy from seed `opener_html`. Autosave note appended automatically.

### Section A — Three variant cards
- 180px thumbnail column (or placeholder if image missing) + body column
- Body: variant rank label ("Variant A"), name, tagline, "What's different" line, "Open live mockup ↗" link in lawn-green underline (target=_blank)
- Footer: three rank buttons (1st / 2nd / 3rd) + two voice-textareas ("What works" + "What doesn't")
- **Rank mutex:** clicking "1st" on Variant B clears "1st" from any other card. Each rank appears at most once across the 3 cards.

### Section B — Deal-breakers (1 card)
- Voice-textarea: "Anything in any of them you genuinely couldn't live with?"
- Always optional — most replies leave it blank.

### Section C — Anything else (1 card, T9 catch-all)
- Voice-textarea: "Anything else in your head about these we haven't asked?"
- Always optional.

### Submit
Standard `submitMission` from app.js. Validates all 3 variant cards have a rank set. Three voice textareas optional. Two prose textareas optional.

## Templates used (from `procedure_reply_tool_templates.md`)

- **T11-adjacent** — variant cards have hero image + body + choice + voice (the spec table is replaced by tagline/diff prose).
- **T9** — final catch-all card.
- **C1** — voice-to-text wired on every textarea.
- **Novel rank-mutex pattern** — candidate **T13** for the registry. Promote to T13 once second mockup-feedback round ships (e.g. when this same shape gets used for a third surface).

## Seed shape (`seed-example.json`)

```json
{
  "surface": "news" | "caq",
  "surface_label": "news.croquetqld.org" | "Queensland Croquet Association",
  "opener_html": "<p>...</p>",
  "variants": [
    {
      "id": "a" | "b" | "c",
      "rank_label": "Variant A",
      "name": "Ghost Source baseline",
      "tagline": "...",
      "diff": "...",
      "url": "https://news-mockup-a.croquetwade.com",
      "thumbnail": "variant-a.png"
    }
  ]
}
```

Per-stakeholder tokens minted via `apps/issue-reply-token.py --mission <slug> --name "..." --email "..." --seed seed-example.json` (or per-surface seed file).

## Forking checklist (Phase 3.1 / 3.2)

1. `cp -r apps/reply-croquetclaude-site/mockup-feedback-template apps/reply-croquetclaude-site/<surface>-mockup-feedback`
2. Capture variant thumbnails (Playwright at 1280×800, save as `variant-{a,b,c}.png` in mission `images/`)
3. Author per-surface seed (`resources/<surface>-mockup-seed.json`) with real URLs + variant copy
4. Mint one token per stakeholder
5. Deploy: `bash apps/deploy-reply-croquetclaude.sh`
6. Drop URLs into per-stakeholder draft emails (Wade reviews per `feedback_draft_before_send.md`)

## Response payload shape

```json
{
  "ranks": [
    { "variant_id": "a", "rank": 1 },
    { "variant_id": "b", "rank": 3 },
    { "variant_id": "c", "rank": 2 }
  ],
  "per_variant": [
    { "variant_id": "a", "what_works": "...", "what_doesnt": "..." },
    { "variant_id": "b", "what_works": "...", "what_doesnt": "..." },
    { "variant_id": "c", "what_works": "...", "what_doesnt": "..." }
  ],
  "deal_breakers": "...",
  "open_comments": "..."
}
```

Phase 4.1 reads these JSON payloads from `reply_mission_responses` and synthesises winning direction per surface.
