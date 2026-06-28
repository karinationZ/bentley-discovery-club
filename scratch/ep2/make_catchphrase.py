#!/usr/bin/env python3
"""Regenerate Bentley's paced catchphrase (Stop. Look. Listen. with pauses) + rebuild the read-through reel.
Run: ELEVENLABS_API_KEY=... python3 scratch/ep2/make_catchphrase.py"""
import sys, os, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.voices.dialogue import tts_catchphrase
OUT = f"{ROOT}/scratch/ep2/vo"

tts_catchphrase(f"{OUT}/B_stoplook.mp3", gap=0.45)
d = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{OUT}/B_stoplook.mp3"]).decode().strip()
print(f"B_stoplook (paced catchphrase): {float(d):.2f}s", flush=True)

ORDER = ["B_hook1","B_hook2","N_intro","B_chase","B_rude","N_camo","B_help","B_realize","B_stoplook",
         "I_stopped","B_why","I_hide","B_snackpouch","N_taste","I_confess","B_colorgame","N_friends",
         "I_hurt","B_breathe","N_boneless","B_button","N_hearts","I_gathering","B_ants","B_stoplook","N_outro"]
sil = f"{OUT}/_sil.mp3"
listf = f"{OUT}/_list.txt"
with open(listf,"w") as f:
    for lab in ORDER:
        f.write(f"file '{OUT}/{lab}.mp3'\nfile '{sil}'\n")
reel = f"{OUT}/EP2_VO_READTHROUGH.mp3"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",listf,"-c:a","libmp3lame","-b:a","192k",reel],check=True)
dt = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",reel]).decode().strip()
print(f"REEL rebuilt: {float(dt):.1f}s -> {reel}", flush=True)
