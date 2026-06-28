#!/usr/bin/env python3
"""Mix Ep2 v7 picture/dialogue to final 1080p master."""
import os
import re
import subprocess
from pathlib import Path

ROOT = Path("/project")
ASM = ROOT / "scratch/ep2/final_v7/assembly"
SEG = ASM / "segs"
MUS = ROOT / "assets/pilot_shots/ep1/v2/music"
SFX = ROOT / "assets/pilot_shots/ep1/v2/sfx"
CUT = ASM / "EP2_v7_PICTURE_DIALOGUE.mp4"
OUT = ASM / "EP2_v7_FINAL.mp4"
AUD = ["-ar", "48000", "-ac", "2"]


def durof(path):
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
        )
        .decode()
        .strip()
    )


segs = []
for f in sorted(os.listdir(SEG)):
    if not re.match(r"^\d{2}_", f) or not f.endswith(".mp4"):
        continue
    stem = f[:-4]
    if stem.endswith("_silent") or stem.endswith("_bg"):
        continue
    segs.append(f)
start = {}
act_dur = {}
t = 0.0
for f in segs:
    sid = f[3:-4]
    act = sid.split("_")[0]
    d = durof(SEG / f)
    start[sid] = t
    act_dur[act] = act_dur.get(act, 0.0) + d
    t += d
total = t
print(f"total {total:.1f}s; acts:", {k: round(v, 1) for k, v in act_dur.items()}, flush=True)

act_cue = {
    "a0": "theme_wonder",
    "a1": "theme_wonder",
    "a2": "suspense",
    "a3": "emotional_piano",
    "a4": "suspense",
    "a5": "emotional_piano",
    "a6": "triumph",
}
parts = []
for act in ["a0", "a1", "a2", "a3", "a4", "a5", "a6"]:
    if act not in act_dur:
        continue
    d = act_dur[act]
    cue = MUS / f"{act_cue[act]}.mp3"
    out = ASM / f"_mus_{act}.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-stream_loop",
            "-1",
            "-i",
            str(cue),
            "-t",
            f"{d:.2f}",
            "-af",
            f"afade=t=in:st=0:d=0.8,afade=t=out:st={max(0, d - 0.8):.2f}:d=0.8",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(out),
        ],
        check=True,
    )
    parts.append(out)

mlist = ASM / "_muslist.txt"
mlist.write_text("\n".join(f"file '{p}'" for p in parts))
music = ASM / "_music.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(mlist), "-ar", "48000", "-ac", "2", str(music)], check=True)

events = [
    ("a0_02_boop", "chime", 0.45),
    ("a0_04_ink_reaction", "octo_curl", 0.45),
    ("a1_07_chase", "shake", 0.45),
    ("a2_11_bolt", "octo_curl", 0.45),
    ("a2_12_eelstir", "shake", 0.35),
    ("a3_14_stoplook", "sparkle", 0.45),
    ("a6_34_ants", "skitter", 0.45),
]
events = [(start[i], s, v) for i, s, v in events if i in start and (SFX / f"{s}.mp3").exists()]
sfxtrk = ASM / "_sfx.wav"
if events:
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for _, s, _ in events:
        cmd += ["-i", str(SFX / f"{s}.mp3")]
    flt = "".join(f"[{i}:a]adelay={int(t * 1000)}|{int(t * 1000)},volume={v}[s{i}];" for i, (t, _, v) in enumerate(events))
    flt += "".join(f"[s{i}]" for i in range(len(events))) + f"amix=inputs={len(events)}:duration=longest:normalize=0,apad=whole_dur={total}[a]"
    subprocess.run(cmd + ["-filter_complex", flt, "-map", "[a]", "-t", f"{total:.2f}", "-ar", "48000", "-ac", "2", str(sfxtrk)], check=True)

amb = SFX / "amb_ocean.mp3"
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(CUT), "-stream_loop", "-1", "-i", str(amb), "-i", str(music)]
amix_in = "[d][amb][mus]"
n = 3
if events:
    cmd += ["-i", str(sfxtrk)]
    amix_in = "[d][amb][mus][sfx]"
    n = 4
fc = (
    "[0:v]scale=1920:1080:flags=lanczos,eq=saturation=1.04:contrast=1.03[v];"
    "[0:a]aresample=48000,volume=1.0[d];"
    "[1:a]aresample=48000,volume=0.10[amb];"
    "[2:a]aresample=48000,volume=0.85[mus];"
    + ("[3:a]aresample=48000,volume=0.9[sfx];" if events else "")
    + f"{amix_in}amix=inputs={n}:duration=first:normalize=0[a]"
)
subprocess.run(
    cmd
    + [
        "-filter_complex",
        fc,
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        *AUD,
        str(OUT),
    ],
    check=True,
)
print(f"FINAL MASTER: {durof(OUT):.1f}s -> {OUT}", flush=True)
