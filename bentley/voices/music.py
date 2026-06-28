#!/usr/bin/env python3
"""Generate the music cue palette via ElevenLabs music API. No fal.
One evolving family of cues for the 11 scored state-changes; placed/crossfaded in assembly."""
import os, json, subprocess, urllib.request, urllib.error
from bentley.shared.eleven import KEY
OUT = "assets/pilot_shots/ep1/v2/music"; os.makedirs(OUT, exist_ok=True)

def music(name, prompt, ms=30000):
    payload = {"prompt": prompt, "music_length_ms": ms}
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music",
        data=json.dumps(payload).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    out = f"{OUT}/{name}.mp3"
    try:
        with urllib.request.urlopen(req, timeout=180) as r, open(out, "wb") as f: f.write(r.read())
        d = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out]).decode().strip()
        print(f"  ok   {name:16s} {d}s", flush=True)
    except urllib.error.HTTPError as e:
        print(f"  FAIL {name}: {e.code} {e.read().decode()[:200]}", flush=True)
    except Exception as e:
        print(f"  ERR  {name}: {e}", flush=True)

CUES = [
 ("calm_mystery",    "Sparse gentle mysterious dawn ambience for a children's nature cartoon, soft lonely piano notes over a calm ocean morning, a simple tender two-note motif, peaceful and a little lonely", 22000),
 ("theme_wonder",    "Warm whimsical orchestral children's adventure theme, light curious strings and woodwinds, gentle wonder and discovery, Pixar-like and hopeful, built on a simple memorable two-note motif", 30000),
 ("emotional_piano", "Intimate tender solo piano with soft held strings for a heartfelt children's film moment, quiet and emotional, gentle sadness lifting gradually into warmth and hope", 28000),
 ("suspense",        "Light playful suspense for a kids' cartoon, building percussion and low strings, a brief scary-but-safe danger moment that resolves, not too frightening", 18000),
 ("triumph",         "Triumphant warm orchestral swell for a children's film, joyful wonder payoff, full bright strings and gentle brass, celebratory and heartwarming", 20000),
]
if __name__ == "__main__":
    for n, p, ms in CUES:
        music(n, p, ms)
    print("MUSIC DONE ->", OUT, flush=True)
