#!/usr/bin/env python3
"""Compose the re-consolidated Ep2 hero keyframes (hero_v2) into one labeled sheet."""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = "/project"
H = f"{ROOT}/scratch/ep2/hero_v2"
PANELS = [
    (f"{H}/s03_rock_eye.png", "#3  ROCK -> EYE"),
    (f"{H}/s14_emergence.png", "#14  Indi emerges (MASTER)"),
    (f"{H}/s20_squeeze.png", "#20  Boneless squeeze"),
    (f"{H}/bentley_cu_awe.png", "Bentley CU (paw tag)"),
    (f"{H}/s22_pawhold.png", "#22  Paw-hold"),
    (f"{H}/s16_exchange.png", "#16  Heart-to-heart"),
    (f"{H}/s16a_colorgame.png", "#16A  Color-game bond"),
]
CW, CH, LBL, PAD, TITLE = 470, 264, 30, 12, 50
COLS, ROWS = 4, 2
def font(s):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, s)
            except Exception: pass
    return ImageFont.load_default()
W = COLS*CW + (COLS+1)*PAD; Ht = TITLE + ROWS*(CH+LBL+PAD) + PAD
sheet = Image.new("RGB", (W, Ht), (245,245,248)); d = ImageDraw.Draw(sheet)
d.text((PAD,12), "Ep2 HERO KEYFRAMES — RE-CONSOLIDATED (final Indi master + Bentley paw tag, Nano Banana Pro)", fill=(30,30,40), font=font(22))
for i,(p,l) in enumerate(PANELS):
    r,c = divmod(i,COLS); x = PAD + c*(CW+PAD); y = TITLE + r*(CH+LBL+PAD)
    try: sheet.paste(Image.open(p).convert("RGB").resize((CW,CH)), (x,y))
    except Exception: d.rectangle([x,y,x+CW,y+CH], fill=(220,220,225))
    d.text((x+6, y+CH+4), l, fill=(40,40,55), font=font(20))
OUT = f"{H}/EP2_HERO_KEYFRAMES_v2.png"; sheet.save(OUT); print("saved:", OUT)
