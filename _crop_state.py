"""Crop state screenshots for closer inspection."""
import os
from PIL import Image

SCREENS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_screens')

for name in ('state-tablet-answered', 'state-tablet-missing'):
    src = os.path.join(SCREENS, f'{name}.png')
    if not os.path.exists(src):
        continue
    img = Image.open(src)
    w, h = img.size
    img.crop((0, 0, w, min(int(h * 0.30), 1700))).save(os.path.join(SCREENS, f'{name}-top.png'))
    print(f'  {name}: top crop saved')
