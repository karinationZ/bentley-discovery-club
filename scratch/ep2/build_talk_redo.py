#!/usr/bin/env python3
"""Ep2 recovery — Stage 3 (talk): re-do the 2 failed Bentley clips + render B_breathe, via the framework
(no-smile prompt, master-derived keyframe). Run: KIE_KEY=... python3 scratch/ep2/build_talk_redo.py"""
import sys
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.character_framework import batch, BENTLEY
from bentley.shared import kie_client

KF = f"{ROOT}/assets/character_design/Bentley_talkkey.png"
VO = f"{ROOT}/scratch/ep2/vo"; OUT = f"{ROOT}/scratch/ep2/talking"
items = [
    (f"{VO}/B_realize.mp3",   f"{OUT}/talk_B_realize.mp4",   "worried"),
    (f"{VO}/B_colorgame.mp3", f"{OUT}/talk_B_colorgame.mp4", "delighted"),
    (f"{VO}/B_breathe.mp3",   f"{OUT}/talk_B_breathe.mp4",   "tender"),
]
print("bal before:", kie_client.credits(), flush=True)
for out, c in batch(BENTLEY, items, keyframe=KF):
    print(f"  {out}: {c}cr" + ("" if c else "  <-- FAILED"), flush=True)
print("bal after:", kie_client.credits(), flush=True)
print("=== TALK REDO DONE ===", flush=True)
