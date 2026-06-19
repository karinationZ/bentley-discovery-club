#!/usr/bin/env python3
"""BRIGHT N6 keyframe via kie.ai nano-banana-edit — high-key daylight + closed mouth (clean avatar input)."""
from kie_client import run, credits, download
MASTER = "https://v3b.fal.media/files/b/0a9eb213/K0YEhgC0hRPAknNVA_bSO_Bentley_MASTER_clean_16x9.png"
PROMPT = ("TIGHT character CLOSE-UP of Bentley the red-fawn Boxer puppy — head and upper chest fill the frame "
 "(head ~60% of frame height, white chest blaze visible at bottom), 85mm portrait, shallow depth of field; behind her "
 "a BRIGHT sunny morning sky and sunlit tide-pool in soft creamy bokeh — luminous pale-gold and soft-blue DAYLIGHT, "
 "bright and airy — NOT foggy, NOT a sunset, NOT an orange dusk horizon, NOT washed out. Near eye-level, subtle "
 "three-quarter head turn toward camera, soulful dark-brown eyes looking warmly INTO camera, tiny affectionate head-tilt. "
 "EXPRESSION: warm, fond, gently content — her mouth GENTLY CLOSED with lips softly together, calm and relaxed — NO open "
 "mouth, NO teeth showing at all, NO pant, NO grin, NO gape. Soft kind eyes "
 "with clear catchlights, faint warm brow-lift. On-model: black mask, grey chin, small white chest blaze ONLY, solid red-fawn "
 "legs and paws (NO white socks), BOTH ears soft floppy folded DOWN, short docked stubby tail, soulful well-proportioned eyes "
 "(NOT googly), teal collar with glowing spiral seashell charm. LIGHTING: BRIGHT, luminous, HIGH-KEY clear morning sunshine — "
 "her whole face evenly and brightly lit, clean highlights on mask/brow/cheek, soft open fill, NO muddy shadows, NO dark "
 "side of the face. Rich, saturated, VIBRANT red-fawn fur, colorful, cheerful high-key daylight. Absolutely NOT dim, NOT moody, "
 "NOT dusk, NOT sunset, NOT backlit, NOT dark. Premium dimensional Pixar/Bluey cartoon, NOT photoreal. Sharp focus on her "
 "brightly lit face. Same dog, match exactly.")
print("bal before:", credits())
r = run("google/nano-banana-edit", {"prompt": PROMPT, "image_urls": [MASTER], "image_size": "16:9", "output_format": "png"})
download(r["urls"][0], "tests/kie/N6_kie_key_bright2.png")
print(f"DONE  credits={r['credits']}  secs={r['secs']}")
print("url:", r["urls"][0])
print("bal after:", credits())
open("tests/kie/N6_bright2_url.txt", "w").write(r["urls"][0])
