#!/usr/bin/env python3
"""Audition ElevenLabs voices for Pip (small fussy hermit crab).
Each candidate is pitched up ~10% (asetrate up + atempo back) to sound small-creature,
with a light clean. Outputs to tests/eleven/pip/."""
import os, json, subprocess, urllib.request
KEY = os.environ["ELEVENLABS_API_KEY"]
SR = 44100
PITCH = 1.10  # +10% -> small crab

def tts(voice_id, text, out):
    body = json.dumps({"text": text, "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.75, "style": 0.65, "speed": 1.05}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_192",
        data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    raw = out.replace(".mp3", "_raw.mp3")
    with urllib.request.urlopen(req) as r, open(raw, "wb") as f: f.write(r.read())
    atempo = round(1/PITCH, 4)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",
        f"asetrate={int(SR*PITCH)},aresample={SR},atempo={atempo},highpass=f=110,equalizer=f=300:t=q:w=1:g=-1,loudnorm=I=-16:TP=-1.5:LRA=11",
        "-b:a","192k",out], check=True)
    print("  ok ->", out, flush=True)

LINE = ("[nervous] Gah! A — a GIANT! Don't squish me, don't eat me — I'm very stringy and I would NOT taste good! "
        "[fussy, deflating] ...And another thing: I am not lost. I know exactly where I am. That is the whole problem.")
CANDS = [("callum", "N2lVS1w4EtoT3dr4eOWO"),   # husky trickster -> quirky grumpy crab
         ("liam",   "TX3LPaxmHKxFdv7VOQHJ"),   # energetic young -> fast nervous patter
         ("will",   "bIHbv24MWmeRgasZH58o")]   # relaxed young -> sweeter/softer crab

os.makedirs("tests/eleven/pip", exist_ok=True)
for name, vid in CANDS:
    print(f"[pip] {name}", flush=True)
    tts(vid, LINE, f"tests/eleven/pip/pip_{name}.mp3")
print("done", flush=True)
