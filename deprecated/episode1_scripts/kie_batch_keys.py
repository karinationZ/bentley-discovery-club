#!/usr/bin/env python3
"""Tier-1 batch PHASE 1 — 3 bright keyframes (a1_02_react, a5_04_tag, N1_guess) via kie nano-banana-edit.
Hosts each on catbox + writes manifest. QA these before Phase 2 (avatars)."""
from kie_client import run, credits, download
import subprocess, json, os
os.makedirs("tests/kie/batch", exist_ok=True)
MASTER = "https://v3b.fal.media/files/b/0a9eb213/K0YEhgC0hRPAknNVA_bSO_Bentley_MASTER_clean_16x9.png"

BRIGHT = (" LIGHTING: BRIGHT, luminous, HIGH-KEY clear morning sunshine — her whole face evenly and brightly lit, clean "
 "highlights on mask/brow/cheek, soft open fill, NO muddy shadows, NO dark side of the face. Rich, saturated, VIBRANT "
 "red-fawn fur, colorful, cheerful high-key daylight. Absolutely NOT dim, NOT moody, NOT dusk, NOT sunset, NOT backlit, NOT dark.")
MODEL = (" On-model: black mask, grey chin, small white chest blaze ONLY, solid red-fawn legs and paws (NO white socks), "
 "BOTH ears soft floppy folded DOWN, short docked stubby tail, soulful well-proportioned eyes (NOT googly), teal collar "
 "with glowing spiral seashell charm. Premium dimensional Pixar/Bluey cartoon, NOT photoreal. Sharp focus on her brightly "
 "lit face. Same dog, match exactly.")
COMMON = BRIGHT + MODEL

SHOTS = {
 "a1_02_react": ("TIGHT CLOSE-UP of Bentley the red-fawn Boxer puppy — head and upper chest fill the frame, 85mm shallow "
   "depth of field, soft bright bokeh tide-pool behind. She has JUST heard a faraway cry: bright SURPRISE turning to "
   "delighted CURIOSITY — eyes WIDE, bright and sparkling, ears perking softly (still folded down), head lifting and "
   "turning toward the sound, a tiny eager gasp. Her mouth softly closed or barely parted, gentle and curious — NO open "
   "gape, NO teeth showing, NO grin. The look of a puppy who just discovered an adventure." + COMMON),
 "a5_04_tag": ("TIGHT warm CLOSE-UP of Bentley the red-fawn Boxer puppy — head and upper chest, 85mm shallow depth of "
   "field, soft bright bokeh behind. Her signature playful, charming moment: a cute gentle HEAD-TILT, soulful eyes "
   "looking warmly and directly INTO camera, a soft friendly GENTLY CLOSED mouth with lips together, a kind warm brow — "
   "adorable, curious, full of personality. NO open mouth, NO teeth, NO grin. This is the shot that makes the audience "
   "fall in love with Bentley." + COMMON),
 "N1_guess": ("CLOSE-UP of Bentley the red-fawn Boxer puppy, framed slightly LOWER and a touch tighter than a standard "
   "portrait (a gentle low push-in feel), head and chest fill the frame. She is delighted and playful, mid happy "
   "guessing — a bright delighted HEAD-TILT to HER LEFT (opposite the usual), sparkling curious eyes, eyebrows up, "
   "bursting with cheerful energy. Her mouth softly closed or barely parted in a happy curious expression — NO open "
   "gape, NO upper teeth, NO human grin. Bright, joyful, full of wonder." + COMMON),
}

manifest = {}
print("bal before:", credits())
for sid, prompt in SHOTS.items():
    r = run("google/nano-banana-edit", {"prompt": prompt, "image_urls":[MASTER], "image_size":"16:9", "output_format":"png"})
    lp = f"tests/kie/batch/{sid}_key.png"
    download(r["urls"][0], lp)
    url = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{lp}",
                                   "https://catbox.moe/user/api.php"]).decode().strip()
    ok = url.startswith("http")
    manifest[sid] = {"local": lp, "cat_url": url if ok else None, "key_credits": r["credits"]}
    print(f"{sid}: {r['credits']}cr {r['secs']}s  catbox={'OK' if ok else 'FAIL:'+url[:60]}")
json.dump(manifest, open("tests/kie/batch/manifest.json","w"), indent=1)
print("bal after:", credits())
