"""Crop screenshots into top/middle/bottom regions for closer inspection."""
import os
import sys
from PIL import Image

SCREENS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_screens')
PHASE = sys.argv[1] if len(sys.argv) > 1 else 'after'

for label in ('phone-375', 'tablet-1024', 'desktop-1440'):
    src = os.path.join(SCREENS, f'{PHASE}-{label}.png')
    if not os.path.exists(src):
        print('skip', src)
        continue
    img = Image.open(src)
    w, h = img.size
    img.crop((0, 0, w, min(int(h * 0.30), 1400))).save(os.path.join(SCREENS, f'{PHASE}-{label}-top.png'))
    mid_top = max(0, int(h * 0.45) - 700)
    mid_bot = min(h, int(h * 0.45) + 700)
    img.crop((0, mid_top, w, mid_bot)).save(os.path.join(SCREENS, f'{PHASE}-{label}-mid.png'))
    img.crop((0, max(0, h - 1400), w, h)).save(os.path.join(SCREENS, f'{PHASE}-{label}-bottom.png'))
    print(f'  {label}: {w}x{h} cropped (top/mid/bottom)')
print('Done.')
