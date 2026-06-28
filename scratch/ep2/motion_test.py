#!/usr/bin/env python3
"""Gate D motion TEST — animate the approved s16_exchange keyframe via Kling 2.6 i2v.
Gentle tender living motion; characters/style preserved (i2v animates the keyframe). 5s clip.
Extracts QA frames afterward. Run: KIE_KEY=... python3 scratch/ep2/motion_test.py
"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

OUT = f"{ROOT}/scratch/ep2/motion"; os.makedirs(OUT, exist_ok=True)
SRC = f"{ROOT}/scratch/ep2/hero_v2/s16_exchange.png"
MP4 = f"{OUT}/s16_exchange_motion.mp4"

def host(p):
    u = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"): raise RuntimeError("catbox fail")
    return u

PROMPT = ("Very subtle, gentle, tender living motion. The octopus Indi's HEAD and FACE stay COMPLETELY STILL and frozen — do "
          "NOT animate, move, open or reshape her mouth or face in any way; her small mouth stays soft and CLOSED exactly as "
          "in the still image; Indi has NO teeth and NO smile at any moment (octopuses have no teeth). Bentley the dog "
          "breathes softly and slow-blinks; her mouth stays a relaxed natural dog mouth, soft and closed (NO human smile, NO "
          "human teeth, NO grin); her floppy ears stay folded DOWN (not flying), keep her Boxer brow wrinkles. ONLY animate: "
          "the octopus's ARMS gently swaying and one arm slowly reaching in the water, soft water ripples and tiny sparkles, "
          "and Bentley's gentle breathing and one slow blink. Warm, calm, tender. Smooth, slow and MINIMAL — locked camera, "
          "no fast motion, no camera shake. Keep the EXACT same characters, colours, proportions, faces, mouths and 3D "
          "rendering style as the still image.")

url = host(SRC); print("input:", url, flush=True)
print("bal before:", kie_client.credits(), flush=True)
ok = False
for i in range(8):
    try:
        r = kie_client.run("kling-2.6/image-to-video",
                           {"prompt": PROMPT, "image_urls": [url], "sound": False, "duration": "5"}, timeout=600)
        kie_client.download(r["urls"][0], MP4)
        print(f"DONE: {r.get('credits')}cr {r.get('secs')}s -> {MP4}", flush=True); ok = True; break
    except Exception as e:
        print(f"  attempt {i+1}: {str(e)[:100]}", flush=True); time.sleep(10)
print("bal after:", kie_client.credits(), flush=True)

if ok:
    # probe + extract QA frames
    dur = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=width,height",
                          "-of","default=noprint_wrappers=1", MP4], capture_output=True, text=True).stdout
    print("clip info:\n"+dur, flush=True)
    for t in ["0.1","1.5","3.0","4.8"]:
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",t,"-i",MP4,"-frames:v","1",
                        f"{OUT}/_qa_{t}.png"], check=False)
    # contact sheet of the 4 frames
    subprocess.run(["ffmpeg","-y","-loglevel","error","-pattern_type","glob","-i",f"{OUT}/_qa_*.png",
                    "-vf","scale=400:-1,tile=4x1", f"{OUT}/_qa_strip.png"], check=False)
    print("QA frames + strip extracted", flush=True)
print("=== MOTION TEST DONE ===", flush=True)
