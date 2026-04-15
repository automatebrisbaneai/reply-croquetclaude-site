"""Screenshot the page in interactive states: with selections + with missing/error."""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_screens')
os.makedirs(OUT, exist_ok=True)
URL = 'http://127.0.0.1:8765/coaching-list-questions/_preview.html'

with sync_playwright() as p:
    browser = p.chromium.launch()

    # 1. Tablet — answered state on first 4 cards (mix of include/drop/unsure)
    ctx = browser.new_context(viewport={'width': 1024, 'height': 768}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto(URL)
    page.wait_for_selector('.card', timeout=10000)
    page.wait_for_timeout(800)

    # Click some answers to see selected states
    page.locator('.card').nth(0).locator('button[data-value="include"]').click()
    page.locator('.card').nth(1).locator('button[data-value="drop"]').click()
    page.locator('.card').nth(2).locator('button[data-value="unsure"]').click()
    page.wait_for_timeout(500)
    # Type into the unsure notes
    page.locator('.card').nth(2).locator('textarea').fill('Need to confirm with Bribie Island secretary.')
    page.wait_for_timeout(300)

    page.screenshot(path=os.path.join(OUT, 'state-tablet-answered.png'), full_page=True)
    print('  tablet-answered ->', OUT)
    ctx.close()

    # 2. Tablet — partial answers + click submit to trigger validation error
    ctx = browser.new_context(viewport={'width': 1024, 'height': 768}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto(URL)
    page.wait_for_selector('.card', timeout=10000)
    page.wait_for_timeout(800)

    page.locator('.card').nth(0).locator('button[data-value="include"]').click()
    # Don't answer the rest; click submit to trigger the highlight on missing cards
    # But submit calls submitMission which will fail without PB. We can't actually
    # trigger the validation flow because submit handler in _preview is real.
    # Instead, manually add .missing class via JS to first few cards for the screenshot.
    page.evaluate("""
        document.querySelectorAll('.card').forEach((c, i) => {
            if (i === 1 || i === 2) c.classList.add('missing');
        });
        const ve = document.querySelector('.validation-error');
        ve.textContent = '2 records still need answers — they\\'re highlighted above.';
        ve.classList.add('visible');
    """)
    page.wait_for_timeout(400)
    page.screenshot(path=os.path.join(OUT, 'state-tablet-missing.png'), full_page=True)
    print('  tablet-missing ->', OUT)
    ctx.close()

    browser.close()
print('Done.')
