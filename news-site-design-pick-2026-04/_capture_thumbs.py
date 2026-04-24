"""
Capture thumbnail screenshots for news-site-design-pick-2026-04 theme cards.
Usage: python _capture_thumbs.py
Saves 400x250 PNG thumbnails to images/
"""
import os
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
os.makedirs(OUT, exist_ok=True)

SITES = [
    ('source',         'https://source.ghost.io',                              'source.png'),
    ('casper',         'https://casper.ghost.io',                              'casper.png'),
    ('dope',           'https://dope.ghost.io',                                'dope.png'),
    ('ruby',           'https://ruby.ghost.io',                                'ruby.png'),
    ('tailwind-nextjs','https://tailwind-nextjs-starter-blog.vercel.app',      'tailwind-nextjs.png'),
    ('fuwari',         'https://fuwari.vercel.app',                            'fuwari.png'),
]

W, H = 1200, 800
THUMB_W, THUMB_H = 400, 250

with sync_playwright() as p:
    browser = p.chromium.launch()
    for slug, url, filename in SITES:
        print(f'Capturing {slug} from {url}...')
        try:
            ctx = browser.new_context(
                viewport={'width': W, 'height': H},
                device_scale_factor=1
            )
            page = ctx.new_page()
            page.goto(url, wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(2500)  # let fonts/images settle

            # Full screenshot then clip to viewport
            tmp_path = os.path.join(OUT, f'_tmp_{slug}.png')
            page.screenshot(path=tmp_path, clip={'x': 0, 'y': 0, 'width': W, 'height': H})
            ctx.close()

            # Resize to thumbnail using PIL if available, else use raw capture
            try:
                from PIL import Image
                img = Image.open(tmp_path)
                img = img.resize((THUMB_W, THUMB_H), Image.LANCZOS)
                out_path = os.path.join(OUT, filename)
                img.save(out_path, 'PNG', optimize=True)
                os.remove(tmp_path)
                print(f'  -> {out_path} ({THUMB_W}x{THUMB_H})')
            except ImportError:
                # No PIL — rename raw file
                import shutil
                out_path = os.path.join(OUT, filename)
                shutil.move(tmp_path, out_path)
                print(f'  -> {out_path} (raw {W}x{H}, PIL not available for resize)')

        except Exception as e:
            print(f'  ERROR capturing {slug}: {e}')
            # Create a placeholder PNG so the card still renders cleanly
            _make_placeholder(OUT, filename, slug)
    browser.close()

def _make_placeholder(out_dir, filename, label):
    """Write a minimal cream-coloured placeholder PNG if PIL is available."""
    try:
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (400, 250), color=(254, 250, 224))
        draw = ImageDraw.Draw(img)
        draw.text((160, 110), '?', fill=(188, 108, 37))
        img.save(os.path.join(out_dir, filename), 'PNG')
        print(f'  -> placeholder written for {label}')
    except Exception:
        pass

print('Done.')
