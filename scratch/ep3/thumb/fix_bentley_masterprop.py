#!/usr/bin/env python3
"""Redraw ONLY Bentley in the EP3 thumbnail base so she matches the MASTER PROP (semi-realistic
Pixar boxer) instead of the current googly-eyed over-cartoon face. Composition, ant, hole, sand,
collar/tag and framing are preserved. Feeds base (composition) + master (identity) to nano-banana-edit.
Run: (set -a; source .env; set +a) then  python3 scratch/ep3/thumb/fix_bentley_masterprop.py"""
from bentley.shared.kie_client import run, download, credits
from bentley.shared.hosting import kie_host

BASE = "scratch/ep3/thumb/ep3_base.png"
MASTER = "assets/character_design/Bentley_MASTER_pixar.png"
OUT = "scratch/ep3/thumb/ep3_base_masterprop.png"

PROMPT = (
    "Image 1 is the scene to keep. Image 2 is the EXACT character reference for Bentley the Boxer puppy. "
    "Redraw ONLY Bentley (the dog filling the right side of image 1) so her head and face match the "
    "character reference in image 2, keeping the same head position, angle, size and the same downward "
    "curious gaze toward the little ant. "
    "FIX the face to the master model: give her NATURAL, realistic warm-brown Boxer eyes like the reference "
    "— iris-dominant with only a little white, gentle and soulful, correctly sized and spaced for a real "
    "puppy. REMOVE the huge cartoon googly bug-eyes and the big white sclera. REMOVE the comic open-mouth "
    "grin and the exposed lower teeth — instead a calm natural dog mouth, closed or barely parted in soft "
    "curiosity (NO human teeth, NO grin). Keep the correct semi-realistic Pixar boxer proportions from the "
    "reference: black mask, grey-and-white chin, warm red-fawn coat, white chest blaze, soft floppy folded "
    "ears, teal collar with the gold paw-shaped 'Bentley' name tag, paws the same color as the coat with no "
    "white socks. "
    "Keep EVERYTHING ELSE in image 1 exactly the same: the small friendly ant on the left, the sandy dune, "
    "the little hole in the sand, the glowing golden spiral trail, the blurred grass, the warm sunset light "
    "and the overall composition and framing. "
    "Match the warm cinematic lighting and the premium dimensional Pixar 3D render style. Photoreal-leaning "
    "cartoon, crisp and poster-quality, 16:9."
)

print("balance:", credits())
base_url = kie_host(BASE)
master_url = kie_host(MASTER)
print("hosted base + master")
r = run("google/nano-banana-edit", {
    "prompt": PROMPT,
    "image_urls": [base_url, master_url],
    "image_size": "16:9",
    "output_format": "png",
})
download(r["urls"][0], OUT)
print(f"done: {r['credits']}cr {r['secs']}s -> {OUT}")
