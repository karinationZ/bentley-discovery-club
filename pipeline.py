#!/usr/bin/env python3
"""Bentley's Discovery Club — production pipeline on the new stack.
Stages per shot: keyframe (Nano-Banana, fal) -> video (Kling 2.5) OR talking (Kling Avatar v2)
                 + voice (ElevenLabs LauraZ v3, cleaned). All locked-design rules baked in.
Resumable: skips a shot whose .mp4 already exists. Per-shot error isolation.
Usage: .venv/bin/python pipeline.py <shotlist.json>

Thin orchestrator. The reusable stages live in the bentley package:
  keyframe / paw_fix -> bentley.asset_generation.keyframes
  video              -> bentley.animation.video
  avatar             -> bentley.animation.avatar
  tts_bentley / pip  -> bentley.voices.dialogue
  fsub / REFS        -> bentley.shared.fal
"""
import json
import os
import sys
import traceback
import urllib.request

import fal_client

from bentley.animation.avatar import avatar
from bentley.animation.video import video
from bentley.asset_generation.keyframes import keyframe, paw_fix
from bentley.voices.dialogue import tts_bentley, tts_pip

ROOT = os.path.dirname(os.path.abspath(__file__))


def dl(url, path):
    urllib.request.urlretrieve(url, path); return path


def produce(shot, work):
    sid = shot["id"]; out = f"{work}/{sid}.mp4"; kpath = f"{work}/{sid}_key.png"
    if os.path.exists(out): print(f"[skip] {sid}"); return out
    print(f"[run] {sid} ({shot['type']})", flush=True)
    if os.path.exists(kpath):
        kf = fal_client.upload_file(kpath); print("      reuse approved keyframe", flush=True)
    else:
        kf = keyframe(shot["keyframe"], shot.get("ref"))
        if shot.get("ref") == "bentley" and shot["type"] == "motion": kf = paw_fix(kf)  # clean paws only on full-body shots
        dl(kf, kpath); print("      keyframe ok", flush=True)
    if os.environ.get("KEYFRAMES_ONLY"):
        print("      keyframe-only -> skip video", flush=True); return kpath
    if shot["type"] == "motion":
        v = video(kf, shot["motion"], shot.get("dur", "5"))
    else:  # talk
        if shot.get("voice") == "bentley":
            a = tts_bentley(shot["line"], f"{work}/{sid}_vo.mp3")
        elif shot.get("voice") == "pip":
            a = tts_pip(shot["line"], f"{work}/{sid}_vo.mp3")
        else:
            a = os.path.join(ROOT, shot["audio_file"])
        au = fal_client.upload_file(a)
        print(f"      audio uploaded", flush=True)
        v = avatar(kf, au)
    dl(v, out)
    print(f"      DONE -> {sid}.mp4", flush=True)
    return out


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    work = os.path.join(ROOT, spec["work"]); os.makedirs(work, exist_ok=True)
    print(f"=== producing {len(spec['shots'])} shots -> {work} ===", flush=True)
    for s in spec["shots"]:
        try: produce(s, work)
        except Exception as e:
            msg = str(e)
            if "Exhausted balance" in msg or "User is locked" in msg or "FAL_TIMEOUT" in msg:
                print("\n!!! FAL BALANCE EXHAUSTED — top up at fal.ai/dashboard/billing, then re-run (resumable; finished shots are skipped). Stopping now.\n", flush=True)
                sys.exit(2)
            print(f"      ERROR {s['id']}: {e}", flush=True); traceback.print_exc()
    print("=== pipeline run complete ===", flush=True)
