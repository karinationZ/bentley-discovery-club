#!/usr/bin/env python3
"""Compose the YouTube thumbnail: punch v1 base + bold outlined 'WHO'S THERE?' (kept fully LEFT of
Bentley's face) + EP tag. 1280x720 JPG."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import os, sys
BASE = sys.argv[1] if len(sys.argv) > 1 else "tests/kie/thumb_v1.png"
OUT  = "tests/kie/Bentley_Ep1_thumbnail.jpg"
W, H = 1280, 720
MAXW = 400   # text must stay within the left column, clear of Bentley's face (her head starts ~x470)
LX   = 46    # left margin

def font(sz):
    for p in ["/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
              "/System/Library/Fonts/Supplemental/Arial Black.ttf",
              "/System/Library/Fonts/SFNSRounded.ttf",
              "/System/Library/Fonts/Supplemental/Chalkboard.ttc"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def fit(lines, maxw, start=168):
    sz = start
    while sz > 50:
        f = font(sz)
        if max(_probe.textlength(ln, font=f) for ln in lines) <= maxw:
            return f, sz
        sz -= 3
    return font(50), 50

img = Image.open(BASE).convert("RGB").resize((W, H), Image.LANCZOS)
img = ImageEnhance.Brightness(img).enhance(1.13)
img = ImageEnhance.Color(img).enhance(1.36)
img = ImageEnhance.Contrast(img).enhance(1.10)
img = ImageEnhance.Sharpness(img).enhance(1.3)

# soft dark vignette in the LEFT column so white text always reads
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(vig).ellipse([-360, -200, 640, 540], fill=(4, 8, 34, 145))
vig = vig.filter(ImageFilter.GaussianBlur(80))
img = Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")

layer = img.convert("RGBA"); d = ImageDraw.Draw(layer)
lines = ["WHO'S", "THERE?"]
f, sz = fit(lines, MAXW)
gap = int(sz * 1.14)
# vertically center the 2-line block in the upper-left
total_h = gap * (len(lines) - 1) + sz
y = 70
sw = max(7, sz // 13)
for ln in lines:
    d.text((LX + 6, y + 8), ln, font=f, fill=(0, 0, 18, 150))                                   # shadow
    d.text((LX, y), ln, font=f, fill=(255, 255, 255, 255), stroke_width=sw, stroke_fill=(24, 18, 74, 255))
    y += gap

# EPISODE 1 tag (bottom-left, teal stroke)
ft = font(48)
d.text((LX + 4, 650), "EPISODE 1", font=ft, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(13, 110, 120, 255))

layer.convert("RGB").save(OUT, quality=92)
print(f"thumbnail -> {OUT}  (text font {sz}px, max line width fits {MAXW}px, right edge ~{LX+MAXW}px)")
