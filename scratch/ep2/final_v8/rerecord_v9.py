#!/usr/bin/env python3
"""Re-record EP2 v9 dialogue fixes (ElevenLabs, locked voices) from the story-editor revision.
Overwrites changed labels + adds new ones in scratch/ep2/vo/. Run: set -a;source .env;set +a; python3 .../rerecord_v9.py
"""
import sys, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import eleven
from bentley.voices.dialogue import tts_bentley, tts_indi
OUT = f"{ROOT}/scratch/ep2/vo"


def tts_bill(text, outp):
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.NARRATOR, text, raw, settings={"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.0})
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                    "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "192k", outp], check=True)
    return outp


LINES = {
    # REWRITES (overwrite existing) ---------------------------------------
    "B_realize":   ("B", "Oh no. I scared her... I chased her straight toward the eel."),
    "B_snackpouch":("B", "A champion, huh? Well, I'm not going anywhere, champ. I'll sit right here — you come out whenever you're ready."),
    "B_colorgame": ("B", "You turned red-fawn — you turned the same color as ME! You're a teeny-tiny ME!"),
    "I_hide":      ("I", "I'm not just hiding — I'm the hide-and-seek CHAMPION! Eight arms, zero bones, never ever been caught! ...You're the very first one who ever found me."),
    "I_confess":   ("I", "I wasn't running from you — I run from everybody. Hiding keeps me safe from the eel. But I kept leaving you those little shells... because I hoped somebody would finally stop, and stay, and listen."),
    "N_hearts":    ("N", "And look at them now — together. You know, our Indi has three hearts, full of blue blood, the copper kind. Her biggest heart even takes a little rest when she swims — so this brave, boneless, color-changing wonder would rather crawl right up beside a friend... and stay."),
    # NEW lines -----------------------------------------------------------
    "I_creep":     ("I", "...You're not chasing me anymore."),                 # replaces I_stopped
    "B_eel":       ("B", "Wait — no — there's something big down there!"),       # eel callout
    "N_shadow":    ("N", "But the reef doesn't stay quiet for long. Somewhere in the rocks... the eel is awake again."),  # eel returns
    "I_colorturn": ("I", "Watch this. I can be... you."),                        # color-game setup
}

for label, (who, text) in LINES.items():
    outp = f"{OUT}/{label}.mp3"
    (tts_bentley if who == "B" else tts_indi if who == "I" else tts_bill)(text, outp)
    d = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", outp]).decode().strip()
    print(f"  {label:13s} [{who}] {float(d):4.1f}s", flush=True)
print("=== re-record done ===", flush=True)
