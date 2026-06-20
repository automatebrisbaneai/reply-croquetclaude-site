"""E2E + screenshots for the committee-vote page.

Usage:
    python _committee_vote_e2e.py <token> [--no-submit]

1. Loads /committee-vote/?t=<token>, waits for cards.
2. Screenshots phone/tablet/desktop (full page) into _screens/.
3. Unless --no-submit: selects a soft answer, a motion answer, all three
   micro agreements + the verdict, fills the general note, submits, and
   asserts the thank-you screen renders.
"""
import sys
import os
from playwright.sync_api import sync_playwright

TOKEN = sys.argv[1] if len(sys.argv) > 1 else ''
NO_SUBMIT = '--no-submit' in sys.argv
if not TOKEN:
    sys.exit("usage: python _committee_vote_e2e.py <token> [--no-submit]")

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_screens')
os.makedirs(OUT, exist_ok=True)
URL = f'http://127.0.0.1:8765/committee-vote/?t={TOKEN}'

VIEWPORTS = [('phone', 375, 850), ('tablet', 1024, 768), ('desktop', 1440, 1000)]

with sync_playwright() as p:
    browser = p.chromium.launch()

    # --- screenshots ---
    for label, w, h in VIEWPORTS:
        ctx = browser.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(URL)
        page.wait_for_selector('.cv-card', timeout=10000)
        page.wait_for_timeout(1200)
        path = os.path.join(OUT, f'committee-vote-{label}-{w}.png')
        page.screenshot(path=path, full_page=True)
        print(f'  shot {label} ({w}x{h}) -> {path}')
        ctx.close()

    if NO_SUBMIT:
        browser.close()
        print('Done (no submit).')
        sys.exit(0)

    # --- interaction + submit ---
    ctx = browser.new_context(viewport={'width': 1024, 'height': 900}, device_scale_factor=1)
    page = ctx.new_page()
    page.goto(URL)
    page.wait_for_selector('.cv-card', timeout=10000)

    # d1 soft -> Sounds right
    page.click('.cv-card[data-id="d1"] .cv-btn[data-value="sounds_right"]')
    # d2 motion -> For
    page.click('.cv-card[data-id="d2"] .cv-btn[data-value="for"]')
    # d3 micro -> all three Agree
    agree_btns = page.query_selector_all('.cv-card[data-id="d3"] .cv-microq .cv-btn.cv-small')
    agrees = [b for b in agree_btns if b.inner_text().strip() == 'Agree']
    for b in agrees:
        b.click()
        page.wait_for_timeout(150)
    # verdict -> That's my position
    page.wait_for_selector('.cv-card[data-id="d3"] .cv-verdict', state='visible', timeout=5000)
    vbtns = page.query_selector_all('.cv-card[data-id="d3"] .cv-verdict .cv-btn')
    for b in vbtns:
        if "position" in b.inner_text().lower():
            b.click()
            break
    # general note
    page.fill('#cv-general', 'E2E test note — please ignore.')
    page.wait_for_timeout(400)

    # all three cards should be marked answered
    answered = page.query_selector_all('.cv-card.cv-answered')
    print(f'  cards marked answered: {len(answered)} (expect 3)')

    page.click('#cv-submit')
    page.wait_for_selector('.thankyou-screen.visible', timeout=10000)
    h1 = page.query_selector('.thankyou-screen h1')
    print('  thank-you shown:', h1.inner_text() if h1 else '(missing)')
    ctx.close()
    browser.close()
    print('Done (submitted).')
