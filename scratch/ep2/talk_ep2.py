#!/usr/bin/env python3
"""Episode 2 talking-shot driver — EPISODE-SPECIFIC config only.

All reusable logic (prompts, rules, anatomy, render pipeline) lives in `bentley.character_framework`.
This file holds only what's unique to Ep2: which lines are talking CUs, their emotion, and the
Ep2 keyframes (each DERIVED FROM the approved master per the consistency rule).

Run: KIE_KEY=... python3 scratch/ep2/talk_ep2.py [bentley|indi|all]

NB: reaction/exclamation lines (B_hook2 "...EYEBALL!", I_hurt "...hurt me!") are NOT talking CUs —
they play as VO over the action shot (the Avatar hallucinates text on short exclamations). See
character_framework rules.LIP_SYNC.
"""
import sys, os
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.character_framework import batch, BENTLEY, INDI

VO = f"{ROOT}/scratch/ep2/vo"
OUT = f"{ROOT}/scratch/ep2/talking"

# (label, emotion) per talking CU
BENTLEY_LINES = [("B_realize", "worried"), ("B_why", "tender"), ("B_snackpouch", "tender"),
                 ("B_colorgame", "delighted"), ("B_button", "tender"), ("B_ants", "stunned"),
                 ("B_stoplook", "calm")]
INDI_LINES = [("I_stopped", "shy"), ("I_hide", "playful"), ("I_confess", "worried"), ("I_gathering", "urgent")]

# Ep2 keyframes — derived FROM the approved masters (Bentley_MASTER_hero.jpg / Indi_LOCKED.png)
KEYFRAMES = {
    "bentley": f"{ROOT}/assets/character_design/Bentley_talkkey.png",
    "indi":    f"{ROOT}/assets/character_design/Indi_openmouth.png",
}


def _items(lines):
    return [(f"{VO}/{lab}.mp3", f"{OUT}/talk_{lab}.mp4", emo) for lab, emo in lines]


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("bentley", "all"):
        print("== Bentley ==")
        for out, c in batch(BENTLEY, _items(BENTLEY_LINES), keyframe=KEYFRAMES["bentley"]):
            print(f"  {out}: {c}cr")
    if which in ("indi", "all"):
        print("== Indi ==")
        for out, c in batch(INDI, _items(INDI_LINES), keyframe=KEYFRAMES["indi"]):
            print(f"  {out}: {c}cr")
