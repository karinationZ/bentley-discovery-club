#!/usr/bin/env python3
"""Best-of-N VO take selection + two-pass loudnorm — the eleven_v3 take-variance fix
(owner law 2026-07-04, playbook Part 2 step 5: identical settings gave a 15x clarity spread).
Score = clarity (4-10kHz share) - 0.15 x |LUFS + 16|; keep the winner; two-pass loudnorm to
exactly -16 LUFS (single-pass undershoots short clips).

Library only — the episode script wires its line list + TTS call and hands a `generate_take`
callable to record_best_of() (usage pattern: scratch/ep4/record_best_of.py):

    def gen(k, take_path):                # k = 1-based take number
        eleven.speak(eleven.BENTLEY, text, raw, settings=B_SET)
        clean_master(raw, take_path)
    best_of.record_best_of(gen, VO / f"{label}.mp3", n=3)
"""
import json
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np

TARGET_LUFS = -16.0
LOUD_PENALTY = 0.15


def clarity(f):
    """4–10kHz energy share (%) — the measured proxy for a crisp, un-muffled take."""
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


def normalize_two_pass(inp, outp, target_i=TARGET_LUFS):
    """Two-pass loudnorm to exactly target_i LUFS (linear mode, measured first pass)."""
    s = lufs_stats(inp)
    af = (f"loudnorm=I={target_i}:TP=-1.5:LRA=11:"
          f"measured_I={s['input_i']}:measured_TP={s['input_tp']}:"
          f"measured_LRA={s['input_lra']}:measured_thresh={s['input_thresh']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(inp), "-af", af,
                    "-ar", "44100", "-b:a", "192k", str(outp)], check=True)


def score(f):
    """clarity − loudness penalty; higher = better take."""
    c = clarity(f)
    s = lufs_stats(f)
    loud_pen = abs(float(s["input_i"]) - TARGET_LUFS) if s else 5.0
    return c - LOUD_PENALTY * loud_pen, c


def record_best_of(generate_take, out_path, n=3, workdir=None):
    """Generate n takes via generate_take(k, take_path), keep the measured best, loudnorm to out_path.
    Returns (best_clarity, [per-take clarity]); raises RuntimeError if every take failed."""
    out_path = Path(out_path)
    with tempfile.TemporaryDirectory(prefix="best_of_", dir=workdir) as td:
        takes = []
        for k in range(1, n + 1):
            take = Path(td) / f"{out_path.stem}_t{k}{out_path.suffix}"
            try:
                generate_take(k, take)
                takes.append((*score(take), take))
            except Exception as e:  # a failed take must not kill the batch — score what exists
                print(f"  {out_path.stem} take{k} FAIL: {str(e)[:90]}", flush=True)
        if not takes:
            raise RuntimeError(f"{out_path.stem}: all {n} takes failed")
        takes.sort(key=lambda t: t[0], reverse=True)
        best = takes[0]
        normalize_two_pass(best[2], out_path)
        print(f"{out_path.stem:20} {' '.join(f'{t[1]:.2f}' for t in takes)} -> {best[1]:.2f}",
              flush=True)
        return best[1], [t[1] for t in takes]
