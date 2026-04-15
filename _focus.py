"""Tight focused crops for finishing-detail review."""
import os
from PIL import Image

SCREENS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_screens')

# tablet-1024 — focus on section C card (4 buttons full-width)
src = os.path.join(SCREENS, 'after-tablet-1024.png')
img = Image.open(src)
w, h = img.size
# Section C is near the bottom — find it via approximate position
# tablet image is ~9440px tall; section C sits roughly 78% down
y0 = int(h * 0.74)
y1 = min(h, int(h * 0.85))
img.crop((0, y0, w, y1)).save(os.path.join(SCREENS, 'after-tablet-1024-sectionC.png'))
print('  tablet section C saved')

# phone-375 — focus on section C
src = os.path.join(SCREENS, 'after-phone-375.png')
img = Image.open(src)
w, h = img.size
y0 = int(h * 0.78)
y1 = min(h, int(h * 0.92))
img.crop((0, y0, w, y1)).save(os.path.join(SCREENS, 'after-phone-375-sectionC.png'))
print('  phone section C saved')

# tablet header isolated
src = os.path.join(SCREENS, 'after-tablet-1024.png')
img = Image.open(src)
w, h = img.size
img.crop((0, 0, w, 220)).save(os.path.join(SCREENS, 'after-tablet-1024-header-only.png'))
print('  tablet header saved')
