"""Screenshot landing page, expired screen, thank-you screen with new styles."""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_screens')

with sync_playwright() as p:
    browser = p.chromium.launch()

    # 1. Index landing page
    ctx = browser.new_context(viewport={'width': 1024, 'height': 768}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto('http://127.0.0.1:8765/')
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(OUT, 'after-landing.png'), full_page=True)
    print('  landing saved')
    ctx.close()

    # 2. 404 / expired
    ctx = browser.new_context(viewport={'width': 1024, 'height': 768}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto('http://127.0.0.1:8765/coaching-list-questions/')  # no token -> expired
    page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(OUT, 'after-expired.png'), full_page=True)
    print('  expired saved')
    ctx.close()

    # 3. Thank-you (synthesise via JS)
    ctx = browser.new_context(viewport={'width': 1024, 'height': 768}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto('http://127.0.0.1:8765/coaching-list-questions/_preview.html')
    page.wait_for_selector('.card', timeout=10000)
    page.evaluate("""
        document.getElementById('app').innerHTML = `
            <div class="thankyou-screen visible">
                <div class="tick">&#10003;</div>
                <h1>Thanks Marilyn — Wade will see your answers right away.</h1>
                <p>You don't need to do anything else.</p>
            </div>
        `;
    """)
    page.wait_for_timeout(500)
    page.screenshot(path=os.path.join(OUT, 'after-thankyou.png'), full_page=True)
    print('  thankyou saved')
    ctx.close()

    browser.close()
print('Done.')
