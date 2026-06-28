#!/usr/bin/env python3
"""VO fix: 'Stop. Look. Listen.' is BENTLEY's catchphrase (was wrongly Narrator). Regenerate it as Bentley,
reword the narrator outro to not use it, rebuild the read-through reel. Run: ELEVENLABS_API_KEY=... python3 ..."""
import sys, os, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import eleven
from bentley.voices.dialogue import tts_bentley
OUT = f"{ROOT}/scratch/ep2/vo"

def tts_bill(text, outp):
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.NARRATOR, text, raw, settings={"stability":0.5,"similarity_boost":0.75,"style":0.4,"speed":1.0})
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",
                    "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11","-b:a","192k",outp], check=True)

# Bentley catchphrase (used at the Turn AND the outro)
tts_bentley("Stop. Look. Listen.", f"{OUT}/B_stoplook.mp3")
# Narrator outro reworded — no catchphrase
tts_bill("And the cove, little friends? It's keeping a very big secret.", f"{OUT}/N_outro.mp3")
print("regenerated B_stoplook + N_outro", flush=True)

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
