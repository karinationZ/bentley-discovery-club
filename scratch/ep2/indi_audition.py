#!/usr/bin/env python3
"""Ep2 GATE B — Indi voice audition. BLIND 5-voice ElevenLabs test (eleven_v3) on her 3 script lines.
Each candidate -> one reel (all 3 lines, 0.6s gaps). Files labeled A-E; name->letter key kept hidden in _key.json.
Uses ElevenLabs (subscription), NOT KIE. Run: ELEVENLABS_API_KEY=... python3 scratch/ep2/indi_audition.py
"""
import sys, os, json, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import eleven

OUT = f"{ROOT}/scratch/ep2/indi_voice"; os.makedirs(OUT, exist_ok=True)

# letter -> (name, voice_id)  [BLIND KEY — not shown to client until they pick]
CANDS = {
    "A": ("Lily",    "pFZP5JQG7iQjIQuC4Bku"),
    "B": ("Sarah",   "EXAVITQu4vr4xnSDxMaL"),
    "C": ("Alice",   "Xb7hH8MSUJpSbSDYk0k2"),
    "D": ("River",   "SAz9YHcvj6GT2YYXdXww"),
    "E": ("Jessica", "cgSgspJ2msm6clMCkdW9"),
}
LINES = [
    "If nobody sees me, nobody can be disappointed by me.",
    "I wasn't running from you. I run from everybody. It's safer to disappear... But I kept leaving you shells because somebody finally needs to listen — the open water's gone wrong.",
    "You don't have to disappear... to be seen by you.",
]
SET = {"stability": 0.4, "similarity_boost": 0.75, "style": 0.45, "speed": 0.95}  # shy/careful, guarded-but-warm

def clean(raw, outp):  # uniform mono/44.1k/loudness so candidates compare fairly + concat cleanly
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-ac", "1", "-ar", "44100",
                    "-af", "highpass=f=90,loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "192k", outp], check=True)

sil = f"{OUT}/_sil.mp3"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                "-t", "0.6", "-ac", "1", "-ar", "44100", "-b:a", "192k", sil], check=True)

key = {}
for L, (name, vid) in CANDS.items():
    parts = []
    for i, txt in enumerate(LINES, 1):
        raw = f"{OUT}/_{L}{i}_raw.mp3"; fin = f"{OUT}/indi_{L}_line{i}.mp3"
        eleven.speak(vid, txt, raw, model="eleven_v3", settings=SET)
        clean(raw, fin); parts.append(fin)
    listf = f"{OUT}/_list_{L}.txt"
    with open(listf, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\nfile '{sil}'\n")
    reel = f"{OUT}/indi_AUDITION_{L}.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listf,
                    "-c:a", "libmp3lame", "-b:a", "192k", reel], check=True)
    key[L] = {"name": name, "voice_id": vid, "reel": reel}
    print(f"{L}: {name} -> {reel}")

json.dump({"settings": SET, "lines": LINES, "key": key}, open(f"{OUT}/_key.json", "w"), indent=1)
print("done. (blind key written to _key.json)")
