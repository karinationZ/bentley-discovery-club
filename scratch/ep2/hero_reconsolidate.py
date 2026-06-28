#!/usr/bin/env python3
"""Re-consolidate Ep2 hero shots from the FINAL locked refs, via Nano Banana Pro (best consistency).
 - Step 1: Bentley master with the new paw 'Bentley' tag (charm-swap).
 - s20 squeeze + Bentley CU + the 3 two-shots: edit from final Indi master + Bentley-pawtag master, lock-to-reference.
 - s14 = the Indi master itself (copy); s03 rock-eye (no face) kept as-is (copy).
Outputs to scratch/ep2/hero_v2/. Retry logic for KIE flakiness.
Run: KIE_KEY=... python3 scratch/ep2/hero_reconsolidate.py
"""
import sys, os, time, shutil, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

OUT = f"{ROOT}/scratch/ep2/hero_v2"; os.makedirs(OUT, exist_ok=True)
INDI_URL = open(f"{ROOT}/assets/character_design/.indi_locked_url.txt").read().strip()
BENT_MASTER = "https://files.catbox.moe/xqf188.png"

def host(p):
    u = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"): raise RuntimeError("catbox fail")
    return u

def runpro(prompt, refs, tries=4):
    for i in range(tries):
        try:
            return kie_client.run("nano-banana-pro",
                {"prompt": prompt, "image_input": refs, "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"})
        except Exception as e:
            print(f"   attempt {i+1}: {str(e)[:80]}", flush=True); time.sleep(6)
    return None

print("bal before:", kie_client.credits(), flush=True)

# --- copies (no gen) ---
shutil.copy(f"{ROOT}/assets/character_design/Indi_LOCKED.png", f"{OUT}/s14_emergence.png")   # master = emergence look
shutil.copy(f"{ROOT}/scratch/ep2/hero/s03_rock_eye.png", f"{OUT}/s03_rock_eye.png")          # camo rock+eye, no face -> keep
print("copied s14 (=master) + s03 (kept)", flush=True)

# --- Step 1: Bentley master with paw tag ---
BENT_TAG = ("Keep Bentley the red-fawn Boxer puppy EXACTLY the same — same dog, same pose, fur, black mask, floppy folded "
            "ears, short docked tail, teal collar, everything. ONLY make sure her collar charm is a small gold PAW-PRINT name "
            "tag engraved 'Bentley' (NOT a seashell). Keep all else identical. Premium Pixar/Bluey 3D, clean, sharp, no grain.")
r = runpro(BENT_TAG, [BENT_MASTER])
BENT_URL = BENT_MASTER
if r:
    bp = f"{OUT}/Bentley_MASTER_pawtag.png"; kie_client.download(r["urls"][0], bp)
    BENT_URL = host(bp); print(f"Bentley pawtag master ({r.get('credits')}cr) -> {bp}\n  hosted {BENT_URL}", flush=True)
else:
    print("Bentley pawtag FAILED -> falling back to plain Bentley master for two-shots", flush=True)

# --- shots ---
SHOTS = {
 "s20_squeeze": ([INDI_URL],
   "Keep THIS octopus (Indi) EXACTLY as in the reference — same face, teal eyes, ocelli, purple colour; do not redraw her. "
   "Restage her POURING her soft boneless purple body through an impossibly tiny coin-size GAP between two wet tide-pool rocks, "
   "arms trailing, determined and focused. She stays SMALL. Bright colorful tide pool, clean, sharp, no grain."),
 "bentley_cu_awe": ([BENT_URL],
   "Keep Bentley (from the reference) EXACTLY the same — same dog, her gold paw-print 'Bentley' name tag, floppy ears, teal "
   "collar; do not redraw her. Restage: a CLOSE-UP of Bentley mid-gasp of WONDER, eyes wide and soulful, natural dog mouth "
   "slightly open (soft pink tongue, small dog teeth, NO human teeth). Bright tide pool, clean, sharp, no grain."),
 "s22_pawhold": ([BENT_URL, INDI_URL],
   "Combine the two reference images into one scene at a bright colorful tide pool. Keep BENTLEY (first image — red-fawn Boxer "
   "with her gold paw-print 'Bentley' name tag, floppy ears, teal collar) and INDI (second image — the small purple octopus, "
   "teal eyes, ocelli) EXACTLY as they are; do not redraw either. POSE: Bentley leans down, whole face in frame, and gently "
   "reaches one front paw toward tiny Indi, whose small purple arm reaches up to touch her paw. Indi is SMALL (about Bentley's "
   "head size). Clean, sharp, no grain. NEGATIVE: redrawing the octopus, eyebrows or nose on the octopus, giant octopus, "
   "cropped dog face, human teeth, film grain."),
 "s16_exchange": ([BENT_URL, INDI_URL],
   "Combine the two references at a bright tide pool. Keep BENTLEY (first image, with her gold paw 'Bentley' tag) and INDI "
   "(second image, small purple octopus) EXACTLY as they are; do not redraw either. POSE: Bentley lies calmly, whole face in "
   "frame, looking down tenderly at tiny Indi who peeks up from the shallow water beside her. Indi is SMALL. Clean, sharp, no "
   "grain. NEGATIVE: redrawing the octopus, eyebrows or nose on octopus, giant octopus, cropped dog face, human teeth, film grain."),
 "s16a_colorgame": ([BENT_URL, INDI_URL],
   "Combine the two references at a bright tide pool. Keep BENTLEY (first image, gold paw 'Bentley' tag) and INDI (second image, "
   "small purple octopus, teal eyes) as they are; do not redraw their faces. POSE: a delighted Bentley (whole face in frame) "
   "beside tiny Indi, who is playfully turning a few RED-FAWN patches across her purple skin to 'match' her friend (keep her "
   "teal eyes + ocelli). Both happy and bonding. Indi is SMALL. Clean, sharp, no grain. NEGATIVE: redrawing the octopus, "
   "eyebrows or nose on octopus, giant octopus, cropped dog face, human teeth, film grain."),
}
for sid, (refs, prompt) in SHOTS.items():
    r = runpro(prompt, refs)
    if r:
        lp = f"{OUT}/{sid}.png"; kie_client.download(r["urls"][0], lp)
        print(f"{sid}: {r.get('credits')}cr {r.get('secs')}s -> {lp}", flush=True)
    else:
        print(f"{sid}: FAILED", flush=True)
print("bal after:", kie_client.credits(), flush=True)
print("=== RE-CONSOLIDATION DONE ===", flush=True)
