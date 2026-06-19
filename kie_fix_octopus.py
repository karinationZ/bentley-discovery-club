#!/usr/bin/env python3
"""Robust octopus render — the extracted-frame catbox URL keeps 422'ing server-side.
Attempt 1: fresh catbox host. Attempt 2: regenerate keyframe via nano-banana (kie-internal URL, always fetchable)."""
from kie_client import run, download
import subprocess
PROMPT_VID = ("A purple octopus tentacle rises up out of the tide-pool, curls and gives a playful little WAVE, then SPLASHES "
 "back down into the water — a big dramatic splash, water droplets and spray flying up catching the golden sunset light, "
 "ripples spreading across the pool. Lively, magical, exciting. Smooth locked camera, no jitter, water fully alive.")
def host(p):
    return subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                    "https://catbox.moe/user/api.php"]).decode().strip()
def try_i2v(url):
    r = run("kling-2.6/image-to-video", {"prompt": PROMPT_VID, "image_urls":[url], "sound": False, "duration":"10"}, timeout=900)
    download(r["urls"][0], "tests/kie/fix/octopus_clip.mp4")
    return r

try:
    u = host("tests/kie/fix/octopus_key.png"); print("attempt1 catbox:", u)
    r = try_i2v(u); print(f"DONE (catbox) octopus: {r['credits']}cr {r['secs']}s")
except Exception as e:
    print("attempt1 failed:", str(e)[:140])
    KPROMPT = ("A friendly cute purple octopus peeking up out of a Crystal Cove tide-pool at golden sunset, one curling "
     "tentacle raised in a playful little wave, big soulful kind eyes, wet black rocks and glassy water around it, warm "
     "golden light, sparkles on the water. Premium dimensional Pixar/Bluey 3D cartoon, colorful, magical, NOT scary.")
    kr = run("google/nano-banana", {"prompt": KPROMPT, "image_size":"16:9", "output_format":"png"})
    ku = kr["urls"][0]; print("attempt2 nano-banana key:", ku); download(ku, "tests/kie/fix/octopus_key2.png")
    r = try_i2v(ku); print(f"DONE (regen) octopus: {r['credits']}cr {r['secs']}s")
