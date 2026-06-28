#!/usr/bin/env python3
"""Audition the client-proposed voice (candidate F) on Indi's 3 lines, same settings as the blind set.
Run: ELEVENLABS_API_KEY=... python3 scratch/ep2/indi_audition_F.py
"""
import sys, os, json, subprocess, urllib.request
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import eleven

VID = "FcZStbCG9g9QxDlJioSD"
OUT = f"{ROOT}/scratch/ep2/indi_voice"; os.makedirs(OUT, exist_ok=True)

# What is this voice?
try:
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/voices/{VID}", headers={"xi-api-key": eleven.KEY})
    info = json.load(urllib.request.urlopen(req))
    print("NAME:", info.get("name"), "| category:", info.get("category"))
    print("labels:", info.get("labels"))
    print("description:", (info.get("description") or "")[:300])
except Exception as e:
    print("voice info fetch failed (may be a public library voice):", str(e)[:160])

LINES = [
    "If nobody sees me, nobody can be disappointed by me.",
    "I wasn't running from you. I run from everybody. It's safer to disappear... But I kept leaving you shells because somebody finally needs to listen — the open water's gone wrong.",
    "You don't have to disappear... to be seen by you.",
]
SET = {"stability": 0.4, "similarity_boost": 0.75, "style": 0.45, "speed": 0.95}

def clean(raw, outp):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-ac", "1", "-ar", "44100",
                    "-af", "highpass=f=90,loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "192k", outp], check=True)

sil = f"{OUT}/_sil.mp3"
if not os.path.exists(sil):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                    "-t", "0.6", "-ac", "1", "-ar", "44100", "-b:a", "192k", sil], check=True)

parts = []
for i, txt in enumerate(LINES, 1):
    raw = f"{OUT}/_F{i}_raw.mp3"; fin = f"{OUT}/indi_F_line{i}.mp3"
    eleven.speak(VID, txt, raw, model="eleven_v3", settings=SET)
    clean(raw, fin); parts.append(fin)
listf = f"{OUT}/_list_F.txt"
with open(listf, "w") as f:
    for p in parts:
        f.write(f"file '{p}'\nfile '{sil}'\n")
reel = f"{OUT}/indi_AUDITION_F.mp3"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listf,
                "-c:a", "libmp3lame", "-b:a", "192k", reel], check=True)
print("F reel ->", reel)
