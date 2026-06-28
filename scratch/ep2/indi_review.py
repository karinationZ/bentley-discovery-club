#!/usr/bin/env python3
"""Side-by-side review of all current Ep2 Indi renders -> spot the inconsistencies."""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = "/project"
PANELS = [
    (f"{ROOT}/assets/character_design/Indi_LOCKED.png", "current lock (v9)"),
    (f"{ROOT}/scratch/ep2/hero/s14_emergence.png", "s14 emergence (LIKED)"),
    (f"{ROOT}/scratch/ep2/hero/s03_rock_eye.png", "s3 rock-eye"),
    (f"{ROOT}/scratch/ep2/hero/s20_squeeze.png", "s20 squeeze"),
    (f"{ROOT}/scratch/ep2/hero/s16_exchange.png", "s16 exchange (drifts)"),
    (f"{ROOT}/scratch/ep2/hero/s16a_colorgame.png", "s16A color-game"),
    (f"{ROOT}/scratch/ep2/indi_sheet/indi_curious.png", "expr curious"),
    (f"{ROOT}/scratch/ep2/indi_sheet/indi_trusting.png", "expr trusting"),
]
CW, CH, LBL, PAD, TITLE = 470, 264, 30, 12, 50
COLS = 4; ROWS = 2
def font(s):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, s)
            except Exception: pass
    return ImageFont.load_default()
W = COLS*CW + (COLS+1)*PAD; Ht = TITLE + ROWS*(CH+LBL+PAD) + PAD
sheet = Image.new("RGB", (W, Ht), (245,245,248)); d = ImageDraw.Draw(sheet)
d.text((PAD,12), "INDI — Ep2 RENDERS REVIEW (consistency check)", fill=(30,30,40), font=font(26))
for i,(p,l) in enumerate(PANELS):
    r,c = divmod(i,COLS); x = PAD + c*(CW+PAD); y = TITLE + r*(CH+LBL+PAD)
    try: sheet.paste(Image.open(p).convert("RGB").resize((CW,CH)), (x,y))
    except Exception: d.rectangle([x,y,x+CW,y+CH], fill=(220,220,225))
    d.text((x+6, y+CH+4), l, fill=(40,40,55), font=font(20))
OUT = f"{ROOT}/scratch/ep2/INDI_REVIEW.png"; sheet.save(OUT); print("saved:", OUT)
