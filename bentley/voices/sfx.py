#!/usr/bin/env python3
"""Generate the SFX palette via ElevenLabs text-to-sound-effects. No fal.
Clips are timeline-independent; trimmed/looped/placed during assembly."""
import os, json, subprocess, urllib.request, urllib.error
from bentley.shared.eleven import KEY
OUT = "assets/pilot_shots/hybrid_ep1/v2/sfx"; os.makedirs(OUT, exist_ok=True)

def sfx(name, text, dur=None, influence=0.4):
    payload = {"text": text, "prompt_influence": influence}
    if dur: payload["duration_seconds"] = dur
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation",
        data=json.dumps(payload).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    out = f"{OUT}/{name}.mp3"
    try:
        with urllib.request.urlopen(req) as r, open(out, "wb") as f: f.write(r.read())
        d = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out]).decode().strip()
        print(f"  ok   {name:12s} {d}s", flush=True)
    except urllib.error.HTTPError as e:
        print(f"  FAIL {name}: {e.code} {e.read().decode()[:140]}", flush=True)

SFX = [
 ("amb_ocean",  "Gentle calm ocean waves washing over a rocky tide pool at dawn, soft continuous peaceful water ambience", 22),
 ("gull",       "A few distant lone seagull cries over a quiet ocean", 4),
 ("chime",      "A soft warm magical gentle bell shimmer, twinkly and short, like a tiny wind chime", 2),
 ("paws",       "Small puppy paws padding and scuffling on wet rock, light quick footsteps", 4),
 ("skitter",    "Tiny crab legs skittering quickly across a wet rock, a nervous little scuttle", 3),
 ("wave_rise",  "An ocean wave building and rising, a growing roar of approaching surf, suspenseful", 5),
 ("wave_crash", "A big ocean wave crashing hard onto rocks with spray and foam, one powerful splash", 4),
 ("shake",      "A wet dog shaking off water fast, droplets spraying everywhere, playful flapping ears", 3),
 ("clicks",     "A row of small hollow shell clicks and taps one after another, rhythmic and satisfying like dominoes", 5),
 ("sparkle",    "A bright magical sparkle shimmer, a twinkle of wonder and discovery", 2),
 ("octo_curl",  "A soft mysterious underwater water curl with a gentle low whoosh", 3),
]
if __name__ == "__main__":
    for item in SFX:
        name, text = item[0], item[1]; dur = item[2] if len(item) > 2 else None
        sfx(name, text, dur)
    print("SFX DONE ->", OUT, flush=True)
