#!/usr/bin/env python3
"""EP2 thumbnail — IDENTICAL text treatment to Ep1 (bentley/asset_generation/thumbnail_text.py) for a
cohesive series look: white fill + navy stroke + soft shadow, left vignette, teal EPISODE tag.
Run: python3 compose_ep2_thumb.py <base.png> [LINE1] [LINE2]"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import os, sys
BASE = sys.argv[1] if len(sys.argv) > 1 else "scratch/ep2/thumbnails/ep2_base_1.png"
LINES = [sys.argv[2], sys.argv[3]] if len(sys.argv) > 3 else ["WHO'S", "HIDING?"]
OUT = "scratch/ep2/thumbnails/EP2_thumbnail.jpg"
W, H = 1280, 720
MAXW = 400
LX = 46


def font(sz):
    for p in ["/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
              "/System/Library/Fonts/Supplemental/Arial Black.ttf",
              "/System/Library/Fonts/SFNSRounded.ttf",
              "/System/Library/Fonts/Supplemental/Chalkboard.ttc"]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
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
# gamma lift FIRST — brightens shadows/mids without blowing highlights -> kills the murk
g = float(os.environ.get("THUMB_GAMMA", "0.80"))
lut = [int(((i / 255.0) ** g) * 255 + 0.5) for i in range(256)] * 3
img = img.point(lut)
img = ImageEnhance.Brightness(img).enhance(float(os.environ.get("THUMB_BRI", "1.10")))
img = ImageEnhance.Color(img).enhance(float(os.environ.get("THUMB_SAT", "1.12")))   # was 1.36 (muddy)
img = ImageEnhance.Contrast(img).enhance(1.03)
img = ImageEnhance.Sharpness(img).enhance(1.45)

# LIGHT navy scrim only behind the title block (top-left) so white text reads — no whole-side murk
vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(vig).ellipse([-380, -260, 520, 360], fill=(6, 10, 40, int(os.environ.get("THUMB_VIG", "78"))))
vig = vig.filter(ImageFilter.GaussianBlur(90))
img = Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")

layer = img.convert("RGBA"); d = ImageDraw.Draw(layer)
f, sz = fit(LINES, MAXW)
gap = int(sz * 1.14)
y = 70
sw = max(7, sz // 13)
for ln in LINES:
    d.text((LX + 6, y + 8), ln, font=f, fill=(0, 0, 18, 150))
    d.text((LX, y), ln, font=f, fill=(255, 255, 255, 255), stroke_width=sw, stroke_fill=(24, 18, 74, 255))
    y += gap

ft = font(48)
d.text((LX + 4, 650), "EPISODE 2", font=ft, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(13, 110, 120, 255))

layer.convert("RGB").save(OUT, quality=92)
print(f"thumbnail -> {OUT}  (font {sz}px, lines {LINES})")
