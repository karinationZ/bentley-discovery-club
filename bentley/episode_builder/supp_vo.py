#!/usr/bin/env python3
"""Supplemental VO for the v2 fix: Theodore intro (4) + 5 Nat-Geo facts (George),
Bentley warmth (LauraZ), Pip callbacks (Callum). ElevenLabs only — no fal."""
import os
from bentley.voices.dialogue import tts_bentley, tts_pip, tts_theo

OUT = "assets/pilot_shots/ep1/v2/audio"; os.makedirs(OUT, exist_ok=True)

THEO = {
 "INTRO1": "Every morning, before the world wakes up... the ocean leaves Crystal Cove full of secrets.",
 "INTRO2": "And THIS... is Bentley. She's not the biggest pup on the beach... but nobody — nobody — is more curious.",
 "INTRO3": "While everyone else just runs right past... Bentley stops. She looks. And she listens.",
 "INTRO4": "Because when you really listen... the whole world starts talking back.",
 "FACT1": "That's Pip — a hermit crab. He's so soft, he has to wear a borrowed seashell like a backpack, and carry his whole house on his back everywhere he goes.",
 "FACT2": "A hermit crab can FEEL when his shell gets too snug — just like outgrowing your favorite shoes. So he has to go shopping for a bigger one.",
 "FACT3": "Here's what the big dog didn't know: little shore crabs like Pip can't swim at all. They WALK on the sea floor — so a big wave isn't fun, it's the scariest thing in the world.",
 "FACT4": "Hermit crabs never waste a good home. When one crab leaves a shell behind, it becomes someone else's brand-new house — the ocean's very own hand-me-downs.",
 "FACT5": "Scientists really do call it a vacancy chain — and they've filmed dozens of real crabs doing it on beaches all over the world. It's true!",
}
BENT = {"snack": "[tender] Aww. I'd never let you be a snack, Pip."}
PIP  = {"n3": "[relieved] Thank you. Thank you. We do NOT do the big water. We've discussed this.",
        "n6allow": "[gruff but pleased] ...It's a shell. ...But I'll allow it."}

if __name__ == "__main__":
    for k, v in THEO.items(): tts_theo(v, f"{OUT}/THEO_{k}.mp3")
    for k, v in BENT.items(): print("  bent ", k, flush=True); tts_bentley(v, f"{OUT}/BENTOS_{k}.mp3")
    for k, v in PIP.items():  print("  pip  ", k, flush=True); tts_pip(v, f"{OUT}/PIPOS_{k}.mp3")
    print("SUPP VO DONE ->", OUT, flush=True)
