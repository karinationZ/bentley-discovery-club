#!/usr/bin/env python3
"""Animate the remaining 6 hero beats via Kling 2.6 i2v, with universal creature/style rules + per-shot action.
Robust retries (KIE flaky). Downloads to scratch/ep2/motion/, extracts dense QA frames per clip.
Run: KIE_KEY=... python3 scratch/ep2/animate_hero.py
"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
HERO = f"{ROOT}/scratch/ep2/hero_v2"
OUT = f"{ROOT}/scratch/ep2/motion"; os.makedirs(OUT, exist_ok=True)
QA = f"{OUT}/qa"; os.makedirs(QA, exist_ok=True)

def host(p):
    u = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"): raise RuntimeError("catbox fail "+p)
    return u

RULES = (" Subtle, gentle, smooth, MINIMAL motion; locked camera, no fast motion, no camera shake. Keep the EXACT same "
         "characters, colours, proportions, faces, mouths and 3D rendering style as the still. NO human smile and NO human "
         "teeth on ANY creature; the octopus Indi's FACE and MOUTH stay frozen and CLOSED with NO teeth and NO smile "
         "(octopuses have no teeth); Bentley keeps her natural dog mouth (closed, or tongue-out exactly as in the still) with "
         "NO human grin; Bentley's floppy ears stay folded DOWN (not flying).")

SHOTS = {
 "s14_emergence":  ("Indi the small purple octopus slowly and shyly creeps a little further out from the dark rock crevice, "
                    "one arm gently reaching and feeling forward, a slow soft blink; gentle water ripples. Timid, hopeful." + RULES),
 "s20_squeeze":    ("Indi gently pours and squeezes her soft boneless body a little way through the narrow gap between the "
                    "rocks, arms slowly trailing through; subtle water movement. Determined, smooth, effortful but gentle." + RULES),
 "s03_rock_eye":   ("On the speckled rock, the single octopus EYE slowly opens and widens and a reddish flush gently deepens "
                    "across the rock surface; a tiny wisp of ink drifts up; subtle water ripple. Mysterious slow reveal." + RULES),
 "bentley_cu_awe": ("Bentley slowly tilts her head a little with wide wondering eyes, soft natural breathing, her pink tongue "
                    "lolling gently, ONE slow blink, ears soft and down. Happy, curious wonder; keep her tongue-out natural "
                    "dog mouth, NO human teeth, NO human grin." + RULES),
 "s22_pawhold":    ("Bentley slowly and gently lowers her paw a touch toward tiny Indi, and Indi slowly raises one arm toward "
                    "Bentley's paw until they almost touch; soft breathing and slow blinks; gentle water ripples. Tender." + RULES),
 "s16a_colorgame": ("Tiny Indi playfully changes colour — soft warm RED-FAWN patches gently bloom across her purple skin "
                    "(mimicking Bentley); her arms sway gently; Bentley watches with soft happy eyes and gentle breathing; "
                    "subtle water. Playful, sweet." + RULES),
}

def render(url, prompt, tries=8):
    for i in range(tries):
        try:
            return kie_client.run("kling-2.6/image-to-video",
                                  {"prompt": prompt, "image_urls": [url], "sound": False, "duration": "5"}, timeout=600)
        except Exception as e:
            print(f"   try {i+1}: {str(e)[:70]}", flush=True); time.sleep(12)
    return None

print("bal before:", kie_client.credits(), flush=True)
for sid, prompt in SHOTS.items():
    kf = f"{HERO}/{sid}.png"
    if not os.path.exists(kf):
        print(f"{sid}: KEYFRAME MISSING", flush=True); continue
    url = host(kf)
    r = render(url, prompt)
    if not r:
        print(f"{sid}: FAILED (KIE)", flush=True); continue
    mp4 = f"{OUT}/{sid}_motion.mp4"; kie_client.download(r["urls"][0], mp4)
    print(f"{sid}: {r.get('credits')}cr {r.get('secs')}s -> {mp4}", flush=True)
    for t in ["0.3","1.0","1.8","2.6","3.4","4.2","4.9"]:
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",t,"-i",mp4,"-frames:v","1",
                        f"{QA}/{sid}_{t}.png"], check=False)
print("bal after:", kie_client.credits(), flush=True)
print("=== HERO ANIMATION BATCH DONE ===", flush=True)
