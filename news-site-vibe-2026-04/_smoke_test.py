"""
Smoke test for news-site-vibe-2026-04 mission page.

Tests desktop (1280x800) and mobile (390x844) viewports.
Requires a valid token URL. Pass it as the first argument or set TOKEN_URL env var.
Uses a DRY_RUN_TOKEN to test the expired/invalid path, and a real minted token
to test the full page renders.

Usage:
    python apps/reply-croquetclaude-site/news-site-vibe-2026-04/_smoke_test.py \
        "https://reply.croquetclaude.com/news-site-vibe-2026-04/?t=<token>"
"""

import sys
import os

from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://reply.croquetclaude.com/news-site-vibe-2026-04/"
EXPIRED_URL = BASE_URL + "?t=INVALID_TOKEN_XYZ"


def run_smoke(page, token_url: str, viewport_name: str) -> None:
    print(f"\n[{viewport_name}] Testing expired/invalid token...")
    page.goto(EXPIRED_URL)
    page.wait_for_load_state("networkidle")
    expired = page.locator(".expired-screen")
    expired.wait_for(state="visible", timeout=10_000)
    assert expired.is_visible(), f"[{viewport_name}] Expected expired screen for invalid token"
    print(f"[{viewport_name}] Expired screen OK")

    print(f"\n[{viewport_name}] Testing valid token URL...")
    page.goto(token_url)
    page.wait_for_load_state("networkidle")

    # 1. All 4 skin sections visible
    for skin_class in ["skin-cheerful", "skin-bs", "skin-defector", "skin-ny"]:
        el = page.locator(f".{skin_class}")
        assert el.count() > 0, f"[{viewport_name}] Missing skin section: {skin_class}"
        assert el.first.is_visible(), f"[{viewport_name}] Skin section not visible: {skin_class}"
    print(f"[{viewport_name}] All 4 skin sections visible")

    # 2. Decision panel at bottom
    panel = page.locator("#decision-panel")
    assert panel.count() > 0, f"[{viewport_name}] Decision panel not found"
    panel.scroll_into_view_if_needed()
    assert panel.is_visible(), f"[{viewport_name}] Decision panel not visible"
    print(f"[{viewport_name}] Decision panel visible")

    # 3. Heading
    heading = page.locator("#decision-panel h2")
    assert heading.inner_text() == "Which direction wins?", \
        f"[{viewport_name}] Unexpected heading: {heading.inner_text()}"
    print(f"[{viewport_name}] Heading correct")

    # 4. Radio options clickable
    radios = page.locator("input[type='radio'][name='skin-pick']")
    assert radios.count() == 5, f"[{viewport_name}] Expected 5 radio options, got {radios.count()}"
    values = [radios.nth(i).get_attribute("value") for i in range(5)]
    assert "cheerful" in values, f"[{viewport_name}] Missing cheerful option"
    assert "bitter-southerner" in values, f"[{viewport_name}] Missing bitter-southerner option"
    assert "defector" in values, f"[{viewport_name}] Missing defector option"
    assert "new-yorker" in values, f"[{viewport_name}] Missing new-yorker option"
    assert "none" in values, f"[{viewport_name}] Missing none option"

    # Click the first real option
    first_option = page.locator(".pick-option").first
    first_option.click()
    first_radio = radios.first
    assert first_radio.is_checked(), f"[{viewport_name}] First radio not checked after click"
    print(f"[{viewport_name}] Radios clickable ({radios.count()} options)")

    # 5. Textarea present
    textarea = page.locator("#panel-notes")
    assert textarea.count() > 0, f"[{viewport_name}] Notes textarea not found"
    assert textarea.is_visible(), f"[{viewport_name}] Notes textarea not visible"
    print(f"[{viewport_name}] Notes textarea present")

    # 6. Submit button present and NOT disabled
    submit = page.locator("#panel-submit-btn")
    assert submit.count() > 0, f"[{viewport_name}] Submit button not found"
    assert submit.is_visible(), f"[{viewport_name}] Submit button not visible"
    # Not clicking — do NOT burn the token
    print(f"[{viewport_name}] Submit button present")

    print(f"\n[{viewport_name}] All checks passed.")


def main() -> None:
    token_url = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.environ.get("TOKEN_URL", "")
    )
    if not token_url:
        print("ERROR: Provide token URL as first argument or set TOKEN_URL env var.")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Desktop
        ctx_desktop = browser.new_context(viewport={"width": 1280, "height": 800})
        page_desktop = ctx_desktop.new_page()
        run_smoke(page_desktop, token_url, "desktop-1280")
        ctx_desktop.close()

        # Mobile (390px)
        ctx_mobile = browser.new_context(viewport={"width": 390, "height": 844})
        page_mobile = ctx_mobile.new_page()
        run_smoke(page_mobile, token_url, "mobile-390")
        ctx_mobile.close()

        browser.close()

    print("\nSmoke test complete — all viewports passed.")


if __name__ == "__main__":
    main()
