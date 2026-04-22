#!/usr/bin/env python3
"""
Desaturation + warm tint pass for culture-papers-round-2 card images.
Same pipeline as Round 1: 60% saturation, +8 red / -8 blue warm tint.
"""

from PIL import Image, ImageEnhance
import os

BASE = os.path.dirname(os.path.abspath(__file__))

CARDS = [
    ("src-card1-patlam.jpg",     "card-1-founding.jpg"),
    ("src-card3-clubs.jpg",      "card-3-clubs.jpg"),
    ("src-card4-chalkboard.jpg", "card-4-selection.jpg"),
]

def warm_tint(img):
    r, g, b = img.split()
    r = r.point(lambda i: min(255, i + 8))
    b = b.point(lambda i: max(0, i - 8))
    return Image.merge("RGB", (r, g, b))

for src_name, dst_name in CARDS:
    src_path = os.path.join(BASE, src_name)
    dst_path = os.path.join(BASE, dst_name)

    print(f"Processing {src_name} -> {dst_name}")
    img = Image.open(src_path).convert("RGB")

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.6)

    img = warm_tint(img)

    img.save(dst_path, "JPEG", quality=90)
    size = os.path.getsize(dst_path)
    print(f"  Saved: {dst_path} ({size // 1024}KB)")

print("\nDone.")
