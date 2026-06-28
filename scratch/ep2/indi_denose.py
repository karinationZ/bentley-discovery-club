#!/usr/bin/env python3
"""Ep2 GATE A — NOSE REMOVAL retouch (targeted edit, not a re-roll).
Negatives weren't removing the nose, so instead we EDIT the existing v7 images with a single instruction:
erase the nose, fill with smooth skin, change nothing else. Hosts each local PNG on catbox, then nano-banana-edit.
Run: KIE_KEY=... python3 scratch/ep2/indi_denose.py
"""
import sys, os, json, subprocess
sys.path.insert(0, "/project")
from bentley.shared import kie_client

OUT = "/project/scratch/ep2/indi_v8_denosed"
os.makedirs(OUT, exist_ok=True)
SRC = {
    "hero": "/project/scratch/ep2/indi_v7/indi_v7_hero.png",
    "peek": "/project/scratch/ep2/indi_v7/indi_v7_peek.png",
}

INSTR = ("Edit this image of a cute cartoon octopus character. REMOVE HER NOSE completely: there is a small nose / nostril "
         "bump between and just below her two eyes — delete it entirely and fill that area with smooth, clean, featureless "
         "purple skin matching the skin around it. An octopus has NO nose. After the edit her face must show ONLY two large "
         "teal eyes and one small soft mouth, with smooth blank purple skin between and below the eyes — absolutely nothing "
         "that looks like a nose, nostrils, a snout or a muzzle. Do NOT change anything else: keep the exact same eyes, the "
         "same small mouth (no teeth), the same purple color and pearlescent sheen, the same low blue ocelli, the same pose, "
         "the same lighting and background. Keep it clean and sharp, no grain.")

def host(p):
    u = subprocess.check_output(["curl", "-s", "-F", "reqtype=fileupload", "-F", f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"):
        raise RuntimeError("catbox fail: " + u[:120])
    return u

print("bal before:", kie_client.credits())
man = {}
for sid, path in SRC.items():
    url = host(path)
    r = kie_client.run("google/nano-banana-edit",
                       {"prompt": INSTR, "image_urls": [url], "image_size": "16:9", "output_format": "png"})
    lp = f"{OUT}/indi_v8_{sid}.png"; kie_client.download(r["urls"][0], lp)
    man[sid] = {"src": path, "src_url": url, "out": lp, "credits": r["credits"], "secs": r["secs"]}
    print(f"{sid}: {r['credits']}cr {r['secs']}s -> {lp}")
json.dump(man, open(f"{OUT}/_denose.json", "w"), indent=1)
print("bal after:", kie_client.credits())
