#!/usr/bin/env python3
"""EP4 MASTER-STYLE CALIBRATION — ONE keyframe (owner-approved 18cr, 2026-07-05).
⚖️ OWNER LAW: model LOCKED = nano-banana-pro for character keyframes. NEVER change the model.
⚖️ STYLE ANCHOR (owner-confirmed): the LITERAL masters — Bentley_MASTER_pixar.png / Bentley_TALKING_MASTER.png.
Ref order matters: MASTER FIRST (style+identity dominates), turnaround, Mira, plate LAST (location only).
No style adjectives from the producer — 'identical to the reference master' is the whole style spec.
Shot: s1b_nose_taste (Mira taps Bentley's nose, cross-eyed delight — 3/4 two-shot)."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
REFS = [f"{CD}/Bentley_MASTER_pixar.png",          # 1 — THE style + identity anchor
        f"{CD}/Bentley_MODEL_SHEET_turnaround.png", # 2 — pose support
        f"{CD}/Mira_LOCKED.png",                    # 3 — Mira design
        f"{CD}/Meadow_plate.png"]                   # 4 — LOCATION ONLY
OUT = os.path.join(os.path.dirname(__file__), "kf_master_cal")
os.makedirs(OUT, exist_ok=True)

PROMPT = (
    "Render Bentley EXACTLY as she appears in the first reference image — same character, same face, same "
    "fur, same eye size and shape, same proportions, and the EXACT same render style, quality, lighting "
    "treatment and finish as that first reference image. Do NOT change or reinterpret the drawing style in "
    "any way; do NOT make her more cartoonish or more realistic; do NOT enlarge her eyes. She has a black "
    "face mask, grey chin, brown eyes, floppy folded-down ears, white chest blaze, short docked tail stub, "
    "teal collar with the gold paw-print tag. CRITICAL: her paws, feet and lower legs are SOLID RED-FAWN, "
    "the exact same color as her coat — NO white paws, NO white socks, NO white toes. "
    "SCENE: a 3/4 two-shot in the coastal wildflower meadow at golden morning (use the last reference image "
    "ONLY for the setting and background): Bentley's head lowered, eyes crossed looking down at her own "
    "nose, where Mira the monarch butterfly (third reference, exactly her locked design) has just landed "
    "and taste-taps it with her feet; Bentley surprised and delighted, about to yelp. 16:9."
)

def main():
    urls = [hosting.catbox_host(p) for p in REFS]
    inp = {"prompt": PROMPT, "image_input": urls, "aspect_ratio": "16:9",
           "resolution": "2K", "output_format": "png"}
    r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=6)
    out = f"{OUT}/s1b_cal.png"
    kie_client.download(r["urls"][0], out)
    print(f"CAL DONE {r['credits']}cr {r['secs']}s -> {out}", flush=True)

if __name__ == "__main__":
    main()
