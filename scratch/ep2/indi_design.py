#!/usr/bin/env python3
"""Ep2 GATE A — Indi v7: REMOVE THE NOSE. Octopuses have no nose — smooth head, no nostrils, no muzzle.
Keeps v6 wins: edit-from-Ep1 anchor (iridescent purple), clean teal non-human eyes (no line), low organic
ocelli below the eyes (real bimac placement), small soft mouth (she talks; no teeth), clean/no-grain.
ONLY change: eliminate the nose / mammal muzzle; smooth face. TOKEN-SMART: 3 keyframes, no video/avatar.
Run: KIE_KEY=... python3 scratch/ep2/indi_design.py
"""
import sys, os, json
sys.path.insert(0, "/project")
from bentley.shared import kie_client

OUT = "/project/scratch/ep2/indi_v7"
os.makedirs(OUT, exist_ok=True)
REF_URL = "https://files.catbox.moe/vk2snn.png"

BODY = ("Indi, a shy, gently-magical young octopus. Skin a deep IRIDESCENT GRAPE-AMETHYST PURPLE with a smooth clean "
        "pearlescent sheen and soft inner subsurface glow; clean smooth skin, NO grain, NO speckle. Rounded soft bell/dome "
        "mantle larger than the eyes; long graceful tapering arms in calm orderly S-curve spirals with soft sucker rows.")

# THE FIX — NO NOSE. An octopus face is smooth.
FACE = ("CRITICAL: an octopus has NO NOSE. Her face is SMOOTH — NO nose, NO nostrils, NO nose bridge, NO muzzle, NO snout, "
        "NO mammal/human face structure. Between and below her eyes the skin is completely smooth purple. The ONLY features "
        "on her face are her two eyes and one small soft mouth.")

EYES = ("Large clean teal eyes set fairly high and lateral on the head, gently bulging like a real octopus: a smooth luminous "
        "TEAL/aqua-cyan iris with a soft simple pupil and ONE small soft catchlight, NO white sclera, NO line or seam across "
        "the eye. An unnatural, magical, NON-HUMAN sea-creature eye color, soulful and gently curious.")

OCELLI = ("Two false-eye spots (ocelli) by real octopus anatomy: ONE small ocellus low on each side of the head, just BELOW "
          "and slightly in front of its real eye near the base of the arms (NOT high on the temples, NOT symmetric headphones) "
          "— a small subtle iridescent-blue chain-link ring in the skin, organic, naturally asymmetric in this 3/4 view, "
          "clearly smaller than the eyes, never glowing.")

MOUTH = ("One small, soft, gentle mouth low on the face — a simple cute creature mouth she can talk and smile with. NO human "
         "teeth, NO human lips, NO grin, NO beak. (It is a mouth, NOT a nose.)")

SET = ("Character-design BUST, head and upper body, three-quarter view. Wet black tide-pool rock and glassy water behind, "
       "BRIGHT warm golden-hour light, vibrant and colorful, CLEAN, SHARP, crisp, high-clarity — modern premium Pixar/Bluey "
       "3D animated kids-series look, smooth clean render. No text, no watermark.")

NEG = ("NEGATIVE — avoid all: nose, NOSE, human nose, animal nose, nostrils, nose bridge, muzzle, snout, mammal face, human "
       "face, dog face, humanoid face, film grain, grain, noise, speckles, sparkle noise, dust, ocelli on the temples, "
       "symmetric eyespots, headphones, glowing rings, LED, line in the eye, seam in the eye, bar pupil, slit pupil, brown "
       "eyes, amber eyes, human or dog eye color, white sclera, eye whites, eyelashes, eyebrows, human teeth, teeth, human "
       "lips, grin, four eyes, red-brown skin, orange, pink, brown body, matte dull skin, rubbery toy, plastic, blue-ringed "
       "octopus, many small rings, baby, chibi, stubby arms, blob, tangled arms, slimy, photoreal, scary, dark, flat 2D, watermark.")

EDIT_PREFIX = ("Using the reference image's iridescent grape-purple color as the base palette (cleaner, no grain), redraw it "
               "as the character below — keep the purple, change pose/expression, and give her a smooth NOSELESS octopus face. ")

VARIANTS = {
    "indi_v7_hero":    "Calm, a shy soulful gaze toward camera, small soft closed smile.",
    "indi_v7_peek":    "Shy PEEK from behind a wet black rock: upper head and eyes visible, one long arm curled softly over the top of her head.",
    "indi_v7_curious": "Curious and gentle, head tilting slightly, one arm reaching forward, mouth a small soft open 'oh' (NO teeth).",
}

print("bal before:", kie_client.credits())
man = {"ref_url": REF_URL}
for sid, expr in VARIANTS.items():
    prompt = EDIT_PREFIX + BODY + " " + FACE + " " + EYES + " " + OCELLI + " " + MOUTH + " " + expr + " " + SET + " " + NEG
    try:
        r = kie_client.run("google/nano-banana-edit",
                           {"prompt": prompt, "image_urls": [REF_URL], "image_size": "16:9", "output_format": "png"})
        method = "edit"
    except Exception as e:
        print(f"{sid}: edit failed ({str(e)[:120]}) -> t2i fallback")
        r = kie_client.run("google/nano-banana", {"prompt": prompt, "image_size": "16:9", "output_format": "png"})
        method = "t2i-fallback"
    lp = f"{OUT}/{sid}.png"; kie_client.download(r["urls"][0], lp)
    man[sid] = {"path": lp, "expr": expr, "method": method, "credits": r["credits"], "secs": r["secs"]}
    print(f"{sid}: [{method}] {r['credits']}cr {r['secs']}s -> {lp}")
json.dump(man, open(f"{OUT}/_candidates.json", "w"), indent=1)
print("bal after:", kie_client.credits())
