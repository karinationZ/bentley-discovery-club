#!/usr/bin/env python3
"""Audition narrator candidates for the permanent 'Grandpa Theodore' voice — same line each."""
import os, json, subprocess, urllib.request, urllib.error
KEY = os.environ["ELEVENLABS_API_KEY"]
OUT = "tests/eleven/narrator"; os.makedirs(OUT, exist_ok=True)
LINE = ("Every morning, before the world wakes up... the ocean leaves Crystal Cove full of secrets. "
        "And this... is Bentley. She's not the biggest pup on the beach — but nobody, nobody, is more curious. "
        "You see, a hermit crab is so soft, he has to carry his whole house on his back... everywhere he goes.")
CANDS = [
 ("George_current", "JBFqnCBsd6RMkjVDRZzb"),   # current narrator (warm storyteller)
 ("Pharaoh_wisdom", "y2Y5MeVPm6ZQXK64WUui"),   # The Pharaoh - Wisdom Bearer (user asked)
 ("Brian_comfort",  "nPczCjzI2devNBz1zQrb"),   # Deep, resonant, comforting
 ("Bill_grandpa",   "pqHfZKP75CvOlQylNhV4"),   # Wise, mature, OLD - most literally grandpa
]
def tts(name, vid):
    body = json.dumps({"text": LINE, "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 0.96}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_192",
        data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    out = f"{OUT}/narr_{name}.mp3"; raw = out.replace(".mp3", "_raw.mp3")
    try:
        with urllib.request.urlopen(req) as r, open(raw, "wb") as f: f.write(r.read())
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",
            "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11","-b:a","192k",out], check=True)
        print(f"  ok   {name:16s} {subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out]).decode().strip()}s")
    except urllib.error.HTTPError as e:
        print(f"  FAIL {name}: {e.code} {e.read().decode()[:160]}")
for n, v in CANDS: tts(n, v)
print("done ->", OUT)
