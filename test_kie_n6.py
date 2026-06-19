#!/usr/bin/env python3
"""kie.ai vs fal test — generate the N6 re-render keyframe (tight warm CU) via kie.ai nano-banana-edit.
Reports credits + seconds. Saves to tests/kie/."""
from kie_client import run, credits, download
import os
os.makedirs("tests/kie", exist_ok=True)
MASTER = "https://v3b.fal.media/files/b/0a9eb213/K0YEhgC0hRPAknNVA_bSO_Bentley_MASTER_clean_16x9.png"
PROMPT = ("TIGHT character CLOSE-UP of Bentley the red-fawn Boxer puppy — head and upper chest fill the frame "
 "(head ~60% of frame height, white chest blaze just visible at the bottom), shot like an 85mm portrait with shallow "
 "depth of field; the tide-pool beach behind her is soft creamy warm-golden bokeh, gently blurred — NOT foggy, NOT hazy, "
 "NOT washed out. Near eye-level looking slightly up at her, subtle three-quarter head turn toward camera, soulful "
 "dark-brown eyes looking warmly INTO the camera, tiny affectionate head-tilt. EXPRESSION: warm, fond, gently amused — "
 "a SOFT closed or barely-open friendly dog mouth, lips relaxed (NOT pulled back at the corners), at most a tiny sliver "
 "of soft pink tongue and small natural LOWER teeth — absolutely NO upper-teeth row, NO lifted upper lip, NO stretched-corner "
 "human grin, NO wide gape. Soft kind eyes with a gentle catchlight and a faint warm brow-lift. On-model: black mask, grey "
 "chin, small white chest blaze ONLY, solid red-fawn legs and paws (NO white socks), BOTH ears soft floppy folded DOWN, "
 "short docked stubby tail, soulful well-proportioned eyes (NOT googly), teal collar with glowing spiral seashell charm. "
 "LIGHTING: warm golden-dawn key raking across her face from camera-left ~30 degrees above eye-line, clean warm highlight on "
 "mask/brow/cheek with soft open fill (no muddy black shadows), soft golden rim along the head/ears. Rich, saturated, VIBRANT "
 "red-fawn fur, colorful and alive, high-contrast, NOT washed out. Premium dimensional Pixar/Bluey cartoon, NOT photoreal. "
 "Sharp focus on her face. Same dog, match exactly.")
print("balance before:", credits())
r = run("google/nano-banana-edit", {"prompt": PROMPT, "image_urls": [MASTER], "image_size": "16:9", "output_format": "png"})
download(r["urls"][0], "tests/kie/N6_kie_key.png")
print(f"DONE  credits={r['credits']}  secs={r['secs']}  tid={r['tid']}")
print("url:", r["urls"][0])
print("balance after:", credits())
