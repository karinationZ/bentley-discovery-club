#!/usr/bin/env python3
"""Generate a CLEAN smooth glowing spiral seashell (NO fur) to replace the furry establish/end shell.
The furry-shell bug = the global 'Pixar soft-fur style' suffix applied to the shell object.
Usage: shell_gen.py            -> keyframe only (QA first)
       shell_gen.py --render   -> also render the motion clip"""
import os, sys, urllib.request, fal_client
M_T2I = "fal-ai/nano-banana"
M_VIDEO = "fal-ai/kling-video/v2.5-turbo/pro/image-to-video"
WORK = "assets/pilot_shots/hybrid_ep1/v2"
KEY = f"{WORK}/CLEAN_shell_key.png"; OUT = f"{WORK}/CLEAN_shell.mp4"

PROMPT = ("A beautiful SMOOTH, GLOSSY, POLISHED pearlescent spiral seashell — a hard porcelain-like "
 "nautilus / moon-snail shell with a clean smooth hard surface — softly glowing warm amber from within, "
 "half-resting on wet black volcanic tide-pool rock at golden dawn; shallow seawater, gentle white foam and "
 "drifting mist around it; soft dawn reflections in the pool. The shell is perfectly SMOOTH and HARD like "
 "polished porcelain or pearl — ABSOLUTELY NO fur, NO hair, NO fuzz, NO soft fibers, NO fluff anywhere on the "
 "shell or rim. Cinematic premium 3D animated render, warm soft light, shallow depth of field, "
 "NOT furry, NOT hairy, NOT fuzzy, NOT painterly, NOT flat. 16:9.")
MOTION = ("The smooth glowing shell rests as gentle waves and white foam wash in and recede around it, the warm "
 "inner glow softly pulses, mist drifts across frame, water ripples and reflects the dawn. Slow smooth push-in, "
 "locked stable camera, no jitter, no shake. The shell surface stays smooth and hard — no fur, no fuzz.")

def keyframe():
    res = fal_client.subscribe(M_T2I, arguments={"prompt": PROMPT, "aspect_ratio": "16:9"})
    url = res["images"][0]["url"]; urllib.request.urlretrieve(url, KEY)
    print("keyframe ->", KEY, flush=True)

def render():
    kf = fal_client.upload_file(KEY)
    res = fal_client.subscribe(M_VIDEO, arguments={"prompt": MOTION, "image_url": kf, "duration": "5", "aspect_ratio": "16:9"})
    urllib.request.urlretrieve(res["video"]["url"], OUT)
    print("clip ->", OUT, flush=True)

if __name__ == "__main__":
    if "--render" in sys.argv: render()
    else: keyframe()
