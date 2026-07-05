#!/usr/bin/env python3
"""Best-of-N VO recording with measured pick (the fix for eleven_v3 take variance).
For each line: N takes -> clean chain -> score (clarity band + loudness distance) -> keep the winner
-> two-pass loudnorm to exactly -16 LUFS. Run: python3 scratch/ep4/record_best_of.py"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, ".")
from bentley.shared import eleven
from bentley.shared.audio import clean_master

VO = Path("scratch/ep4/vo")
N = 3

# every Bentley story line (expressive re-record) + the 3 flagged Mira lines. Catchphrases stay locked.
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location("mv", "scratch/ep4/make_vo.py")
mv = module_from_spec(spec); spec.loader.exec_module(mv)
TODO = [(l, s, t) for l, s, t in mv.LINES
        if s == "B" or l in ("M_dontknow", "M_giggle1", "M_ridewithme")]

B_SET = {"stability": 0.25, "similarity_boost": 0.75, "style": 0.85, "speed": 1.15}
M_SET = {"stability": 0.45, "similarity_boost": 0.9, "style": 0.3}


def clarity(f):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "44100",
                        "-f", "f32le", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, dtype=np.float32)
    if len(a) < 4410:
        return 0.0
    sp = np.abs(np.fft.rfft(a)) ** 2
    fr = np.fft.rfftfreq(len(a), 1 / 44100)
    tot = sp[(fr > 100) & (fr < 16000)].sum()
    return float(100 * sp[(fr > 4000) & (fr < 10000)].sum() / tot) if tot else 0.0


def lufs_stats(f):
    p = subprocess.run(["ffmpeg", "-i", str(f), "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"\{[^}]+\}", p.stderr, re.S)
    return json.loads(m.group(0)) if m else None


def normalize_two_pass(inp, outp):
    s = lufs_stats(inp)
    af = ("loudnorm=I=-16:TP=-1.5:LRA=11:"
          f"measured_I={s['input_i']}:measured_TP={s['input_tp']}:"
          f"measured_LRA={s['input_lra']}:measured_thresh={s['input_thresh']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(inp), "-af", af,
                    "-ar", "44100", "-b:a", "192k", str(outp)], check=True)


print(f"{'line':15} takes(clarity) -> pick")
for label, spk, text in TODO:
    final = VO / f"{label}.mp3"
    takes = []
    for k in range(1, N + 1):
        raw = VO / f"{label}_t{k}_raw.mp3"
        cln = VO / f"{label}_t{k}.mp3"
        try:
            if spk == "B":
                eleven.speak(eleven.BENTLEY, text, str(raw), settings=B_SET)
            else:
                t2 = re.sub(r"\[[^\]]*\]\s*", "", text)
                eleven.speak(eleven.MIRA, t2, str(raw), model="eleven_multilingual_v2", settings=M_SET)
            clean_master(str(raw), str(cln))
            c = clarity(cln)
            s = lufs_stats(cln)
            loud_pen = abs(float(s["input_i"]) + 16) if s else 5.0
            takes.append((c - 0.15 * loud_pen, c, cln))
        except Exception as e:
            print(f"  {label} take{k} FAIL: {str(e)[:90]}", flush=True)
    if not takes:
        print(f"{label:15} ALL TAKES FAILED — kept old file", flush=True)
        continue
    takes.sort(reverse=True)
    best = takes[0]
    normalize_two_pass(best[2], final)
    print(f"{label:15} {' '.join(f'{t[1]:.2f}' for t in takes)} -> {best[1]:.2f}", flush=True)
    for _, _, f in takes:  # tidy take files
        Path(f).unlink(missing_ok=True)
    for k in range(1, N + 1):
        (VO / f"{label}_t{k}_raw.mp3").unlink(missing_ok=True)
print("BEST-OF DONE", flush=True)
