"""Screenshot the handicaps-explainer (scroll-snap layout)."""
import os
import time
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_screens')
os.makedirs(OUT, exist_ok=True)
URL = 'http://127.0.0.1:8765/handicaps-explainer/'
PANELS = ['s1', 's2', 's3', 's4', 's5', 'end']

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Desktop 1440x900 — per-section + full-page
    ctx = browser.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto(URL)
    time.sleep(1.0)
    for i, pid in enumerate(PANELS):
        page.evaluate(f"document.getElementById('{pid}').scrollIntoView({{behavior: 'instant', block: 'start'}})")
        time.sleep(0.6)
        page.screenshot(path=os.path.join(OUT, f'desktop-{i+1}-{pid}.png'))
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.4)
    page.screenshot(path=os.path.join(OUT, 'desktop-fullpage.png'), full_page=True)
    ctx.close()

    # Mobile 390x844 — per-section
    ctx = browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto(URL)
    time.sleep(1.0)
    for i, pid in enumerate(PANELS):
        page.evaluate(f"document.getElementById('{pid}').scrollIntoView({{behavior: 'instant', block: 'start'}})")
        time.sleep(0.5)
        page.screenshot(path=os.path.join(OUT, f'mobile-{i+1}-{pid}.png'))
    ctx.close()

    browser.close()

print('done')
