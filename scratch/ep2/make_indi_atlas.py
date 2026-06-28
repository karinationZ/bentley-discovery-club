#!/usr/bin/env python3
"""Build Indi's TOOTHLESS viseme mouth atlas — 4 mouth shapes, head identical, only the mouth differs.
Edited from Indi_openmouth via Nano-Banana Pro. Run: KIE_KEY=... python3 scratch/ep2/make_indi_atlas.py"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
OUT = f"{ROOT}/scratch/ep2/atlas"; os.makedirs(OUT, exist_ok=True)
BASE = "https://files.catbox.moe/6xzwy3.png"   # Indi_openmouth.png

PRE = ("Keep this octopus Indi EXACTLY the same — identical head position, size, angle, teal eyes, ocelli, iridescent purple "
       "colour, lighting and background. Do NOT move or redraw anything except her mouth. Change ONLY her mouth to: ")
POST = " The mouth interior must be a smooth, soft, dark toothless opening — absolutely NO teeth, NO gums, NO lips, NO smile."
SHAPES = {
 "closed": "a fully CLOSED mouth, just a soft gentle closed seam with no opening at all.",
 "small":  "a SMALL, barely-open soft mouth — a tiny soft dark opening.",
 "mid":    "a MEDIUM soft round open mouth, a gentle 'oh' shape.",
 "wide":   "a WIDE-open soft surprised mouth, a big soft 'OH' shape.",
}
print("bal before:", kie_client.credits())
for name, desc in SHAPES.items():
    outp = f"{OUT}/indi_{name}.png"
    for i in range(4):
        try:
            r = kie_client.run("nano-banana-pro", {"prompt": PRE+desc+POST, "image_input": [BASE],
                                                   "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"})
            kie_client.download(r["urls"][0], outp); print(f"  {name:7s} {r.get('credits')}cr -> {outp}"); break
        except Exception as e:
            print(f"  {name} try {i+1}: {str(e)[:70]}"); time.sleep(6)
print("bal after:", kie_client.credits())
print("=== ATLAS DONE ===")
