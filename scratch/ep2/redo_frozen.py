#!/usr/bin/env python3
"""Re-do the 5 face-prominent silent beats with FROZEN faces/mouths (no teeth). Animate only body/arms/water/colour.
Kling 2.6 i2v, robust retries. Extracts 16 frames/clip for full-res QA. Run: KIE_KEY=... python3 scratch/ep2/redo_frozen.py
"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
HERO = f"{ROOT}/scratch/ep2/hero_v2"
OUT = f"{ROOT}/scratch/ep2/motion"; QA = f"{OUT}/qa2"; os.makedirs(QA, exist_ok=True)

RULES = (" Locked camera, minimal, smooth, slow motion; no fast motion, no camera shake. NO teeth on ANY creature, NO human "
         "smile (octopus Indi has NO teeth). Keep the EXACT same characters, colours, proportions, FACES, MOUTHS, eyes, "
         "ocelli and 3D rendering style as the still image — only the parts named below may move.")

FREEZE = "Keep the character's HEAD, FACE and MOUTH COMPLETELY FROZEN exactly as in the still — do NOT move, open or reshape the mouth or face at all. "
FREEZE2 = "Keep BOTH Bentley's and Indi's HEADS, FACES and MOUTHS COMPLETELY FROZEN exactly as in the still — do NOT move, open or reshape either mouth or face at all. "

SHOTS = {
 "bentley_cu_awe": (FREEZE + "Animate ONLY: her floppy ears shifting very softly, gentle body breathing, and the background "
                    "tide-pool water shimmering. The mouth/tongue stay exactly as the still." + RULES),
 "s14_emergence":  (FREEZE + "Animate ONLY: her boneless body slowly creeping a little further out of the rock crevice and "
                    "one arm gently reaching forward; soft water ripples." + RULES),
 "s20_squeeze":    (FREEZE + "Keep her two ocelli as fixed facial markings — do NOT let any ring slide onto her arms or body. "
                    "Animate ONLY: her soft body and arms gently squeezing and pouring through the narrow gap; soft water." + RULES),
 "s22_pawhold":    (FREEZE2 + "Animate ONLY: Bentley's front paw lowering slightly and Indi's one arm rising toward it until "
                    "they nearly touch; gentle water ripples." + RULES),
 "s16a_colorgame": (FREEZE2 + "Animate ONLY: Indi's skin colour gently shifting — soft warm red-fawn patches blooming across "
                    "her purple skin — and her arms swaying softly; gentle water." + RULES),
}

def render(url, prompt, tries=8):
    for i in range(tries):
        try:
            return kie_client.run("kling-2.6/image-to-video",
                                  {"prompt": prompt, "image_urls": [url], "sound": False, "duration": "5"}, timeout=600)
        except Exception as e:
            print(f"   try {i+1}: {str(e)[:70]}", flush=True); time.sleep(12)
    return None

def host(p):
    u = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"): raise RuntimeError("catbox fail")
    return u

print("bal before:", kie_client.credits(), flush=True)
for sid, prompt in SHOTS.items():
    url = host(f"{HERO}/{sid}.png")
    r = render(url, prompt)
    if not r:
        print(f"{sid}: FAILED", flush=True); continue
    mp4 = f"{OUT}/{sid}_motion.mp4"; kie_client.download(r["urls"][0], mp4)
    print(f"{sid}: {r.get('credits')}cr {r.get('secs')}s -> {mp4}", flush=True)
    for n in range(16):
        t = round(0.3 + n*0.3, 1)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(t),"-i",mp4,"-frames:v","1",
                        f"{QA}/{sid}_{t}.png"], check=False)
print("bal after:", kie_client.credits(), flush=True)
print("=== FROZEN REDO DONE ===", flush=True)
