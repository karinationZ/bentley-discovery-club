#!/usr/bin/env python3
"""Ep2 VO — generate all dialogue + narration with the LOCKED voices, and a full read-through reel (script order).
Bentley=LauraZ (tts_bentley), Indi=locked (tts_indi), Narrator=Bill (eleven_v3, grandpa settings).
Run: ELEVENLABS_API_KEY=... python3 scratch/ep2/make_vo.py
"""
import sys, os, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import eleven
from bentley.voices.dialogue import tts_bentley, tts_indi
OUT = f"{ROOT}/scratch/ep2/vo"; os.makedirs(OUT, exist_ok=True)

def tts_bill(text, outp):
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.NARRATOR, text, raw,
                 settings={"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.0})
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",
                    "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11","-b:a","192k",outp], check=True)
    return outp

# label -> (who, text)
LINES = {
 "B_hook1":     ("B", "Helloooo, little rock. You look like you need... a boop."),
 "B_hook2":     ("B", "The ROCK had an EYEBALL!"),
 "N_intro":     ("N", "That's Bentley. When Bentley meets a mystery, she has one big rule: don't just watch it -- catch it. And that little glow on her collar? That's her Listening Tag. When Bentley holds still, and truly listens, it lights up, and the world whispers its secrets. Trouble is... Bentley's not very good at still. Not yet."),
 "B_chase":     ("B", "Gotcha! Nope. Gotcha! ...Rock. Gotcha--!"),
 "B_rude":      ("B", "Okay. That one was rude."),
 "N_camo":      ("N", "An octopus can change her color AND her texture faster than you can blink -- smooth to spiky, grey to gold -- to vanish into rock, coral, or sand. The greatest hide-and-seek champion in the sea."),
 "B_help":      ("B", "Hey -- hey, it's okay, I just wanna help--"),
 "B_realize":   ("B", "...I chased her right at it."),
 "N_stoplook":  ("N", "Stop. Look. Listen."),
 "I_stopped":   ("I", "...You stopped."),
 "B_why":       ("B", "Why do you keep hiding?"),
 "I_hide":      ("I", "If nobody sees me... nobody can be disappointed by me."),
 "B_snackpouch":("B", "...Okay. That one hit me right in the snack pouch. But I'm not leaving. I'll just sit here. You come out when you're ready."),
 "N_taste":     ("N", "And here's a secret: an octopus can taste by touch. Nearly two-thirds of her thinking happens in her arms -- so when Indi holds your paw, she's not just feeling you. She's reading you."),
 "I_confess":   ("I", "I wasn't running from you. I run from everybody. It's safer to disappear. But I kept leaving you those shells... because somebody finally needs to listen. The open water -- it's gone wrong."),
 "B_colorgame": ("B", "You did -- you did ME! You're a tiny ME!"),
 "N_friends":   ("N", "Two new friends. One can change into anything in the sea... and chose to look like a dog."),
 "I_hurt":      ("I", "No--! You'll hurt me--!"),
 "B_breathe":   ("B", "Okay. Okay. You don't need me to pull. Remember what you are? You don't have bones. You can pour yourself out -- just breathe."),
 "N_boneless":  ("N", "It's true -- the only hard part of an octopus is her tiny beak. Everything else is boneless. Give her a hole bigger than that beak -- about the size of a coin -- and she can squeeze her whole self through it. The real escape artist."),
 "B_button":    ("B", "You don't have to disappear to be safe with me. I SEE you. And you're not scary, OR small. You're amazing."),
 "N_hearts":    ("N", "Three hearts. Blue blood -- real blue, the copper kind. The biggest heart even takes a little rest when she swims... which is why this brave, boneless, color-changing wonder would rather crawl right up beside a friend, and stay."),
 "I_gathering": ("I", "There's a gathering. You have to see. Look -- inland."),
 "B_ants":      ("B", "Wait -- where are you all GOING?"),
 "N_outro":     ("N", "Stop. Look. Listen, little friends. The cove is keeping a very big secret."),
}
ORDER = ["B_hook1","B_hook2","N_intro","B_chase","B_rude","N_camo","B_help","B_realize","N_stoplook",
         "I_stopped","B_why","I_hide","B_snackpouch","N_taste","I_confess","B_colorgame","N_friends",
         "I_hurt","B_breathe","N_boneless","B_button","N_hearts","I_gathering","B_ants","N_outro"]

for label,(who,text) in LINES.items():
    outp = f"{OUT}/{label}.mp3"
    if who == "B": tts_bentley(text, outp)
    elif who == "I": tts_indi(text, outp)
    else: tts_bill(text, outp)
    d = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",outp]).decode().strip()
    print(f"  {label:13s} [{who}] {float(d):4.1f}s", flush=True)

# read-through reel (script order, 0.6s gaps), normalized mono
sil = f"{OUT}/_sil.mp3"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i","anullsrc=r=44100:cl=mono","-t","0.6","-ac","1","-ar","44100","-b:a","192k",sil],check=True)
listf = f"{OUT}/_list.txt"
with open(listf,"w") as f:
    for lab in ORDER:
        f.write(f"file '{OUT}/{lab}.mp3'\nfile '{sil}'\n")
reel = f"{OUT}/EP2_VO_READTHROUGH.mp3"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",listf,"-c:a","libmp3lame","-b:a","192k",reel],check=True)
dt = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",reel]).decode().strip()
print(f"READ-THROUGH REEL: {float(dt):.1f}s -> {reel}", flush=True)
print("=== VO DONE ===", flush=True)
