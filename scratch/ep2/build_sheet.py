#!/usr/bin/env python3
"""Compose Indi's model sheet (front + side + 5 expression/color states) into one labeled 4x2 contact sheet."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "/project"
SH = f"{ROOT}/scratch/ep2/indi_sheet"
PANELS = [
    (f"{ROOT}/assets/character_design/Indi_LOCKED.png", "FRONT (locked)"),
    (f"{SH}/indi_side.png", "SIDE"),
    (f"{SH}/indi_shy.png", "SHY"),
    (f"{SH}/indi_curious.png", "CURIOUS"),
    (f"{SH}/indi_trusting.png", "TRUSTING"),
    (f"{SH}/indi_scared.png", "SCARED (pale)"),
    (f"{SH}/indi_flush_red.png", "STARTLED (red flush)"),
    (f"{SH}/indi_camouflage.png", "CAMOUFLAGE (red-brown)"),
]
CW, CH = 470, 264          # cell image size
LBL, PAD, TITLE = 30, 12, 54
COLS, ROWS = 4, 2

def font(sz):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

W = COLS * CW + (COLS + 1) * PAD
H = TITLE + ROWS * (CH + LBL + PAD) + PAD
sheet = Image.new("RGB", (W, H), (245, 245, 248))
d = ImageDraw.Draw(sheet)
d.text((PAD, 14), "INDI  —  Ep2 guest octopus  ·  MODEL SHEET & EXPRESSION SET", fill=(30, 30, 40), font=font(28))

for i, (path, label) in enumerate(PANELS):
    r, c = divmod(i, COLS)
    x = PAD + c * (CW + PAD)
    y = TITLE + r * (CH + LBL + PAD)
    try:
        im = Image.open(path).convert("RGB").resize((CW, CH))
        sheet.paste(im, (x, y))
    except Exception as e:
        d.rectangle([x, y, x + CW, y + CH], fill=(220, 220, 225)); d.text((x + 8, y + 8), f"missing: {label}", fill=(150, 0, 0), font=font(16))
    d.text((x + 6, y + CH + 4), label, fill=(40, 40, 55), font=font(20))

OUT = f"{ROOT}/assets/character_design/Indi_MODEL_SHEET.png"
sheet.save(OUT)
print("saved:", OUT, sheet.size)
