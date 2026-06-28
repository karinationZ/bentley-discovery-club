#!/usr/bin/env python3
"""Regenerate the two changed VO lines (cheerful new Indi line + Bentley's warm reply).
Run: ELEVENLABS_API_KEY=... python3 scratch/ep2/vo_relines.py"""
import sys, os, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.voices.dialogue import tts_indi, tts_bentley
OUT = f"{ROOT}/scratch/ep2/vo"

tts_indi("I'm not hiding -- I'm the hide-and-seek CHAMPION! Eight arms, zero bones, completely undefeated! ...You're the first one who's ever found me.",
         f"{OUT}/I_hide.mp3")
tts_bentley("Well, I'm not leaving. I'll just sit right here. Come out whenever you're ready... champ.",
            f"{OUT}/B_snackpouch.mp3")
for lab in ("I_hide", "B_snackpouch"):
    d = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{OUT}/{lab}.mp3"]).decode().strip()
    print(f"{lab}: {float(d):.1f}s")
