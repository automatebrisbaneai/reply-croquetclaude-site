#!/usr/bin/env python3
"""
Desaturation + warm tint pass for culture-papers-round-1 card images.
- Reduces saturation ~40% (i.e. leaves 60% of original saturation)
- Adds a slight warm tint (lift reds slightly, cool blues slightly)
- Saves as final filenames in same directory
"""

from PIL import Image, ImageEnhance, ImageOps
import os

BASE = os.path.dirname(os.path.abspath(__file__))

CARDS = [
    ("src-card1-haka.jpg",       "card-1-frame.jpg"),
    ("src-card2-meninga.jpg",    "card-2-coopetition.jpg"),
    ("src-card3-chalkboard.jpg", "card-3-artefact.jpg"),
    ("src-card4-patlam.jpg",     "card-4-small-room.jpg"),
    ("src-card5-mentor.jpg",     "card-5-deviance.jpg"),
]

def warm_tint(img):
    """
    Apply a very slight warm tint by boosting reds +8 and reducing blues -8
    on a per-channel basis. Subtle enough to unify the set without colour-grading feel.
    """
    r, g, b = img.split()
    # Boost red channel slightly
    r = r.point(lambda i: min(255, i + 8))
    # Leave green unchanged
    # Cool blue slightly
    b = b.point(lambda i: max(0, i - 8))
    return Image.merge("RGB", (r, g, b))

for src_name, dst_name in CARDS:
    src_path = os.path.join(BASE, src_name)
    dst_path = os.path.join(BASE, dst_name)

    print(f"Processing {src_name} -> {dst_name}")
    img = Image.open(src_path).convert("RGB")

    # Step 1: Reduce saturation to 60% of original (i.e. ~40% reduction)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.6)

    # Step 2: Apply warm tint
    img = warm_tint(img)

    # Save as JPEG, high quality
    img.save(dst_path, "JPEG", quality=90)
    size = os.path.getsize(dst_path)
    print(f"  Saved: {dst_path} ({size // 1024}KB)")

print("\nDone. All 5 images processed.")
