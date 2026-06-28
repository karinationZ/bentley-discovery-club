#!/usr/bin/env python3
"""Re-record EP2 v10 dialogue deltas from the cinematic v2 revision (EPISODE2_SCRIPT_v2.md §3).
Only the 5 trimmed narrator lines + 1 new Bentley line change; everything else is reused from v9.
Run: set -a; source .env; set +a; python3 scratch/ep2/final_v10/rerecord_v10.py
"""
import sys, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import eleven
from bentley.voices.dialogue import tts_bentley
OUT = f"{ROOT}/scratch/ep2/vo"


def tts_bill(text, outp):
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.NARRATOR, text, raw, settings={"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.0})
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                    "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "192k", outp], check=True)
    return outp


LINES = {
    # trimmed narrator lines (spread over living angles in the cut) -----------------
    "N_camo":   ("N", "Watch closely. An octopus can change her color AND her texture in the blink of an eye -- grey to gold, smooth to spiky -- and melt right into the rock. The greatest hide-and-seek champion in the sea."),
    "N_taste":  ("N", "And here's a little secret. An octopus tastes by touching -- most of her thinking happens right in her arms. So when Indi holds your paw... she isn't just feeling you. She's reading you."),
    "N_hearts": ("N", "And look at them now. Three hearts, full of blue blood -- the copper kind. Her biggest heart even rests a little when she swims... so this boneless, color-changing wonder would rather crawl right up beside a friend... and stay."),
    "N_outro":  ("N", "The cove is keeping a very big secret."),
    "N_friends":("N", "Two new friends. One can change into anything in the whole sea... and chose to look like a dog."),
    # new Bentley line over the lunge (the chase needs an "I can't catch this!" beat) -
    "B_lunge":  ("B", "Wait -- come back! How do you DO that?!"),
}

for label, (who, text) in LINES.items():
    outp = f"{OUT}/{label}.mp3"
    (tts_bentley if who == "B" else tts_bill)(text, outp)
    d = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", outp]).decode().strip()
    print(f"  {label:10s} [{who}] {float(d):4.1f}s", flush=True)
print("=== v10 re-record done ===", flush=True)
