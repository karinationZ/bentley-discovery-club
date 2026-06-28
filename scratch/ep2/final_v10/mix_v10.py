#!/usr/bin/env python3
"""Mix Ep2 v10 -> 1080p master: music beds by mood-run, ambience, SFX, ducked under dialogue, open/close
fade folded in. Run AFTER assemble_v10.py."""
import os, re, subprocess
from pathlib import Path

ROOT = Path("/project")
ASM = ROOT / "scratch/ep2/final_v10/assembly"
SEG = ASM / "segs"
MUS = ROOT / "assets/pilot_shots/ep1/v2/music"
SFX = ROOT / "assets/pilot_shots/ep1/v2/sfx"
CUT = ASM / "EP2_v10_PICTURE_DIALOGUE.mp4"
OUT = ASM / "EP2_v10_FINAL.mp4"
AUD = ["-ar", "48000", "-ac", "2"]


def durof(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode().strip())


def mood(bid):
    n = int(bid[:2])
    if n <= 9:   return "theme_wonder"
    if n <= 14:  return "suspense"
    if n <= 26:  return "emotional_piano"
    if n <= 31:  return "suspense"
    if n <= 33:  return "emotional_piano"
    return "triumph"


SFX_AT = {
    "02_eye": ("octo_curl", 0.45), "05_chase": ("shake", 0.4), "07_camo": ("sparkle", 0.45),
    "11_bolt": ("octo_curl", 0.4), "12_eelpath": ("shake", 0.5), "13_eel": ("shake", 0.45),
    "15_stoplook": ("sparkle", 0.45), "30_squeeze": ("octo_curl", 0.4), "35_ants": ("skitter", 0.45),
}

segs = sorted(f for f in os.listdir(SEG) if re.match(r"^\d{2}_", f) and f.endswith(".mp4"))
start, t, runs = {}, 0.0, []
for f in segs:
    bid = f[:-4]; d = durof(SEG / f); start[bid] = t
    m = mood(bid)
    if runs and runs[-1][0] == m:
        runs[-1][1] += d
    else:
        runs.append([m, d])
    t += d
total = t
print(f"total {total:.1f}s; runs:", [(m, round(d, 1)) for m, d in runs], flush=True)

parts = []
for i, (m, d) in enumerate(runs):
    o = ASM / f"_mus_{i}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", str(MUS / f"{m}.mp3"),
                    "-t", f"{d:.2f}", "-af", f"afade=t=in:st=0:d=0.8,afade=t=out:st={max(0,d-0.8):.2f}:d=0.8", *AUD, str(o)], check=True)
    parts.append(o)
(ASM / "_muslist.txt").write_text("\n".join(f"file '{p}'" for p in parts))
music = ASM / "_music.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(ASM / "_muslist.txt"), *AUD, str(music)], check=True)

events = [(start[b], s, v) for b, (s, v) in SFX_AT.items() if b in start and (SFX / f"{s}.mp3").exists()]
sfxtrk = ASM / "_sfx.wav"
if events:
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for _, s, _ in events:
        cmd += ["-i", str(SFX / f"{s}.mp3")]
    flt = "".join(f"[{i}:a]adelay={int(tt*1000)}|{int(tt*1000)},volume={v}[s{i}];" for i, (tt, _, v) in enumerate(events))
    flt += "".join(f"[s{i}]" for i in range(len(events))) + f"amix=inputs={len(events)}:duration=longest:normalize=0,apad=whole_dur={total}[a]"
    subprocess.run(cmd + ["-filter_complex", flt, "-map", "[a]", "-t", f"{total:.2f}", *AUD, str(sfxtrk)], check=True)

amb = SFX / "amb_ocean.mp3"
fo = total - 0.6
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(CUT), "-stream_loop", "-1", "-i", str(amb), "-i", str(music)]
amix_in, n = "[d][amb][mus]", 3
if events:
    cmd += ["-i", str(sfxtrk)]; amix_in, n = "[d][amb][mus][sfx]", 4
fc = (
    f"[0:v]scale=1920:1080:flags=lanczos,eq=saturation=1.05:contrast=1.03,fade=t=in:st=0:d=0.5,fade=t=out:st={fo:.2f}:d=0.6[v];"
    "[0:a]aresample=48000,volume=1.0[d];[1:a]aresample=48000,volume=0.09[amb];[2:a]aresample=48000,volume=0.80[mus];"
    + ("[3:a]aresample=48000,volume=0.9[sfx];" if events else "")
    + f"{amix_in}amix=inputs={n}:duration=first:normalize=0,afade=t=out:st={fo:.2f}:d=0.6[a]"
)
subprocess.run(cmd + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", *AUD, str(OUT)], check=True)
print(f"FINAL MASTER: {durof(OUT):.1f}s -> {OUT}", flush=True)
