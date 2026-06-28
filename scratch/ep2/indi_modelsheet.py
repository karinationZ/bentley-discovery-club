#!/usr/bin/env python3
"""Ep2 — Indi MODEL SHEET + EXPRESSION/COLOR set. Edits FROM the re-locked Indi master (v9, lateral eyes)
so every panel is the same character. Builds: side turnaround + shy/curious/trusting/scared/startled-flush
expressions + red-brown camouflage state. 7 keyframes (~28 cr). Then tiles a model sheet if ImageMagick is present.
Run: KIE_KEY=... python3 scratch/ep2/indi_modelsheet.py
"""
import sys, os, json, subprocess
sys.path.insert(0, "/project")
from bentley.shared import kie_client

ROOT = "/project"
OUT = f"{ROOT}/scratch/ep2/indi_sheet"
os.makedirs(OUT, exist_ok=True)
LOCKED = f"{ROOT}/assets/character_design/Indi_LOCKED.png"

def host(p):
    u = subprocess.check_output(["curl", "-s", "-F", "reqtype=fileupload", "-F", f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"):
        raise RuntimeError("catbox fail: " + u[:120])
    return u

KEEP = ("This is the LOCKED octopus character Indi — keep her EXACT design and identity: octopus-first, teal lateral eyes "
        "(no white sclera, no line/seam), NO nose, NO nostrils, NO eyebrows, NO human face, one tiny soft lipless mouth (no "
        "teeth), two low iridescent-blue chain-link ocelli just below the eyes, eight tapering suckered arms, iridescent "
        "grape-purple jewel skin. Clean, sharp, colorful, NO grain. Keep her the same character; change ONLY the following: ")

PANELS = {
 "side":      "show a clean SIDE PROFILE turnaround view, full body from the side, calm neutral expression, plain soft tide-pool background — for a character model sheet.",
 "shy":       "a SHY expression: eyelids lowered, one arm curled up over the side of her head, mantle dipped low, skin slightly dimmed, timid and hopeful.",
 "curious":   "a CURIOUS expression: teal pupils wide and dilated, head tilting and leaning in, one arm reaching forward to point, bright and interested.",
 "trusting":  "a TRUSTING warm-happy expression: soft relaxed eyes, a gentle rosy-purple happiness bloom in her skin, one arm gently extended toward a friend, content.",
 "scared":    "a SCARED/anxious moment: her skin DESATURATES to a pale ghostly grey-lavender, small papillae bumps rise, both blue ocelli flare brighter, arms pulled in tight, body shrinking back.",
 "flush_red": "a STARTLED FLASH: her skin flushes DEEP RED for an instant, teal eyes wide, arms splaying outward in surprise.",
 "camouflage":"CAMOUFLAGE state: her skin turns mottled RED-BROWN and bumpy (papillae) to blend into a speckled tide-pool rock she rests on, nearly disappearing — only one teal eye gives her away.",
}

print("re-hosting locked master...")
url = host(LOCKED); print("LOCKED_URL:", url)
open(f"{ROOT}/assets/character_design/.indi_locked_url.txt", "w").write(url + "\n")

print("bal before:", kie_client.credits())
man = {"locked_url": url}
for sid, instr in PANELS.items():
    try:
        r = kie_client.run("google/nano-banana-edit",
                           {"prompt": KEEP + instr, "image_urls": [url], "image_size": "16:9", "output_format": "png"})
        lp = f"{OUT}/indi_{sid}.png"; kie_client.download(r["urls"][0], lp)
        man[sid] = {"path": lp, "credits": r["credits"], "secs": r["secs"]}
        print(f"{sid}: {r['credits']}cr {r['secs']}s -> {lp}")
    except Exception as e:
        man[sid] = {"error": str(e)[:200]}; print(f"{sid}: FAILED {str(e)[:200]}")
json.dump(man, open(f"{OUT}/_sheet.json", "w"), indent=1)
print("bal after:", kie_client.credits())

# Optional: tile a model sheet (front + panels) if ImageMagick montage exists
panels = [LOCKED] + [man[s]["path"] for s in PANELS if "path" in man.get(s, {})]
try:
    subprocess.run(["montage", *panels, "-tile", "4x2", "-geometry", "+6+6", "-background", "white",
                    f"{OUT}/indi_model_sheet.png"], check=True)
    print("model sheet ->", f"{OUT}/indi_model_sheet.png")
except Exception as e:
    print("montage skipped (ImageMagick not found?):", str(e)[:80])
