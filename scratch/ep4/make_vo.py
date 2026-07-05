#!/usr/bin/env python3
"""EP4 'The Butterfly Highway' — record the full VO reel to scratch/ep4/vo/<label>.mp3.
Voices (LOCKED): Bentley=LauraZ (tts_bentley, v3+tags OK) · Mira=eleven.MIRA (tts_mira, mlv2,
tags auto-stripped) · Narrator=Bill (v3, his own gentle chain). Catchphrases via tts_catchphrase.
All dialogue passes the committed 'D bright' clean_master chain. Run: python3 scratch/ep4/make_vo.py"""
import json
import os
import subprocess
import sys
import urllib.request

sys.path.insert(0, ".")
from bentley.shared.eleven import KEY, NARRATOR as BILL
from bentley.voices.dialogue import tts_bentley, tts_mira, tts_catchphrase

OUT = "scratch/ep4/vo"
os.makedirs(OUT, exist_ok=True)


def tts_bill(text, outp):
    body = json.dumps({"text": text, "model_id": "eleven_v3",
                       "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.0}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{BILL}?output_format=mp3_44100_192",
        data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    raw = outp.replace(".mp3", "_raw.mp3")
    with urllib.request.urlopen(req) as r, open(raw, "wb") as f:
        f.write(r.read())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                    "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "192k", outp], check=True)
    return outp


LINES = [
 ("B_hook1",       "B", "[gasps] Whoa -- WHOA. The sky is... the sky is ORANGE. Is the sky okay??"),
 ("B_hook2",       "B", "[laughing] It's RAINING butterflies! [thrilled] Best! Morning! EVER!"),
 ("B_hooknose",    "B", "[surprised] Hey -- you landed on my nose! [giggling] Wait... did you just TASTE my nose? With your FEET?"),
 ("M_hello",       "M", "Mmm-hm! Sandy... salty... adventure-y! You taste like FUN. I'm Mira!"),
 ("B_iam",         "B", "[bright, happy] And I'm Bentley!"),
 ("N_intro",       "N", "Big heart, bigger nose -- that's our Bentley. And her brand-new friend? The bravest little pilot in a whole sky of wings... off on the longest adventure of her life."),
 ("M_comeon",      "M", "Come ON, slowpoke! This way!"),
 ("B_plan",        "B", "[excited] Ooh, an adventure! Okay -- where are we going? Do we have a map? A plan? [hopeful] ...snacks?"),
 ("M_nomap",       "M", "No map! The sun knows the way -- we just follow the fun!"),
 ("B_nomap2",      "B", "[baffled] No map. She said no map. [laughing] That is NOT usually how I-- hey, WAIT UP!"),
 ("N_feet",        "N", "Here's a little secret: a butterfly tastes with her FEET. The moment Mira lands on a flower, her toes know if it's sweet."),
 ("M_trythis",     "M", "Land on one! Toes first! Now -- is it sweet?"),
 ("B_copyfeet",    "B", "[determined] Toes first. Okay. [confused] I taste... foot. And pollen. [building up] Ah -- ah -- AH-CHOO!"),
 ("M_giggle1",     "M", "You're doing it wrong!"),
 ("B_questions",   "B", "[dizzy, delighted] I have SO many questions, and exactly zero of them are about snacks now. That's new!"),
 ("B_lead",        "B", "[confident] You know what this adventure needs? A LEADER! [charging off] Follow me, Mira -- I'll get us there super fast!"),
 ("N_race",        "N", "But butterflies never race. Bentley huffed, and puffed, and bounded ahead..."),
 ("M_floptease",   "M", "Found you! Great leading! You led us right into the flowers!"),
 ("B_flop",        "B", "[dizzy] I'm helping-- I'm totally hel-- oof! [deadpan] I regret the flowers. [happy] Worth it. Still regret it."),
 ("N_turn",        "N", "And when Bentley finally got still... she really SAW it."),
 ("B_river",       "B", "[hushed wonder] They're not racing at all. They're FLOATING -- all leaning the same way, toward the sun. [amazed] It's a whole RIVER of butterflies."),
 ("B_wheredoesit", "B", "[curious] But Mira -- where does it END? How do you even KNOW the way?"),
 ("M_dontknow",    "M", "I don't! Nobody does!"),
 ("M_generations", "M", "My great-grandma started this trip. My kids' kids will finish it! We each just fly to the next flower... and trust the family."),
 ("B_mindblown",   "B", "[awed] You don't know where you're going... and you're having the BEST time?? [joyful] That is the most DOG thing I've ever heard. I LOVE it!"),
 ("N_generations", "N", "And that's the Butterfly Highway -- a road built by great-grandmothers, one flower at a time."),
 ("M_ridewithme",  "M", "Warm wind's coming up -- ride it with me!"),
 ("M_glidecoach",  "M", "Ears out! Legs in! Let the wind do the flying!"),
 ("B_glide",       "B", "[nervous then whooping] I'm gliding-- I'm GLIDING! Okay, this is WAY better than running!"),
 ("N_updraft",     "N", "On a warm rising breeze, a dog and a butterfly caught the very same golden current."),
 ("B_grove",       "B", "[breathless] ...Whoa. Look at them ALL."),
 ("M_home",        "M", "Everybody who ever followed the next flower... ends up right here. Home!"),
 ("N_grove",       "N", "Thousands of monarchs, gathering in the old coast groves, wing to wing, keeping each other cozy and warm."),
 ("B_worm",        "B", "[scandalized, delighted] Hold on. Hold ON. You -- little Miss Sparkle-Wings -- used to be a crawly little WORM?"),
 ("M_caterpillar", "M", "A CATERPILLAR! I built a tiny green room, took the world's longest nap... and woke up with WINGS!"),
 ("B_fancyworm",   "B", "[amazed] Best! Trick! EVER! [eager] Teach me -- I nap ALL the time. I am SO ready!"),
 ("N_button",      "N", "Every butterfly began as a caterpillar who tucked into a tiny green case... and rebuilt herself, top to tail, into a pair of wings."),
 ("N_dusk",        "N", "That night, deep in the whispering grove... the whole orange sky came home to sleep."),
 ("M_goodnight",   "M", "Night, Bentley. Not bad... for a dog who can't even fly!"),
 ("B_reflect",     "B", "[sleepy, content] Y'know what, Mira? Today I stopped bossing... and I looked... and I really listened. [yawn] Best... day... ever."),
 ("M_grovesong",   "M", "Mm-hm. Now sleep. When the night wind comes through... the old grove likes to SING."),
 ("B_dreamy",      "B", "[drowsy, mumbling] ...singing trees... that's the good kind of weird..."),
 ("B_mantra",      "B", "[whispering, sleepy] Stop... look... listen... [softer, drifting to sleep] Stop... look... listen..."),
 ("N_close",       "N", "[soft, warm] Sleep snug, little friends. Tomorrow... the trees have a secret to tell."),
]

if __name__ == "__main__":
    fn = {"B": tts_bentley, "M": tts_mira, "N": tts_bill}
    for label, spk, text in LINES:
        outp = f"{OUT}/{label}.mp3"
        if os.path.exists(outp):
            print(f"skip {label} (exists)", flush=True)
            continue
        try:
            fn[spk](text, outp)
            d = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", outp]).decode().strip()
            print(f"{label:15} {spk} {float(d):5.2f}s", flush=True)
        except Exception as e:
            print(f"FAIL {label}: {str(e)[:130]}", flush=True)
    # the two catchphrase reads (Bentley only, single-utterance method)
    for label in ("B_stoplook",):
        outp = f"{OUT}/{label}.mp3"
        if not os.path.exists(outp):
            try:
                tts_catchphrase(outp)
                print(f"{label:15} B (catchphrase)", flush=True)
            except Exception as e:
                print(f"FAIL {label}: {str(e)[:130]}", flush=True)
    print("VO REEL DONE", flush=True)
