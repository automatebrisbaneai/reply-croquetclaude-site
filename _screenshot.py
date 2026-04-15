"""Screenshot the reply form preview at 3 viewports.

Usage:
    python _screenshot.py before
    python _screenshot.py after
"""
import sys
import os
from playwright.sync_api import sync_playwright

PHASE = sys.argv[1] if len(sys.argv) > 1 else 'before'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_screens')
os.makedirs(OUT, exist_ok=True)

URL = 'http://127.0.0.1:8765/coaching-list-questions/_preview.html'

VIEWPORTS = [
    ('phone', 375, 800),
    ('tablet', 1024, 768),
    ('desktop', 1440, 900),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for label, w, h in VIEWPORTS:
        ctx = browser.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2)
        page = ctx.new_page()
        page.goto(URL)
        # Wait for content to render
        page.wait_for_selector('.card', timeout=10000)
        page.wait_for_timeout(1200)  # let fonts settle
        path = os.path.join(OUT, f'{PHASE}-{label}-{w}.png')
        page.screenshot(path=path, full_page=True)
        print(f'  {label} ({w}x{h}) -> {path}')
        ctx.close()
    browser.close()
print('Done.')
