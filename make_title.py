#!/usr/bin/env python3
"""Title card for the intro: 'BENTLEY'S BIG ADVENTURES' wordmark on transparent PNG
(overlaid on the dawn establish shot, fades in/out). Brand colors + bold rounded font."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1920, 1080
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

def load(sz):
    for p in ["/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
              "/System/Library/Fonts/Supplemental/Futura.ttc",
              "/System/Library/Fonts/Avenir Next.ttc",
              "/System/Library/Fonts/SFNSRounded.ttf",
              "/Library/Fonts/Arial Bold.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except Exception: continue
    return ImageFont.load_default()

def centered(text, font, cy, fill, stroke_fill, stroke_w):
    bb = d.textbbox((0, 0), text, font=font, stroke_width=stroke_w)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    d.text(((W-tw)/2 - bb[0], cy - th/2 - bb[1]), text, font=font,
           fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_w)

NAVY = (11, 59, 87, 255); TEAL = (26, 167, 160, 255)
GOLD = (251, 191, 61, 255); WHITE = (255, 255, 255, 255)

# main wordmark (two lines for impact)
f1 = load(150)
centered("BENTLEY'S", f1, H*0.40, WHITE, NAVY, 10)
centered("BIG ADVENTURES", f1, H*0.54, GOLD, NAVY, 10)
# tagline
f2 = load(54)
centered("Explore     Discover     Wonder", f2, H*0.66, TEAL, NAVY, 6)
# draw two small gold dots as separators (font lacks the interpunct glyph)
for cx in (W*0.5 - 118, W*0.5 + 118):
    d.ellipse([cx-6, H*0.66-6, cx+6, H*0.66+6], fill=GOLD)

out = "/home/user/src/youtube/assets/pilot_shots/hybrid_ep1/v2/work/title_card.png"
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out)
print("title card ->", out, img.size)
