#!/usr/bin/env python3
"""Stitch all talking shots into one review reel (script order). Normalizes to 1280x720. Run: python3 ..."""
import os, subprocess
ROOT = "/project"
T = f"{ROOT}/scratch/ep2/talking"
TMP = f"{T}/_reel"; os.makedirs(TMP, exist_ok=True)

# (label, file) in rough script order
CLIPS = [
 ("B_realize",    f"{T}/talk_B_realize.mp4"),
 ("B_stoplook",   f"{T}/talk_B_stoplook.mp4"),
 ("I_stopped",    f"{T}/talk_I_stopped.mp4"),
 ("B_why",        f"{T}/talk_B_why.mp4"),
 ("I_hide(champ)",f"{T}/_indi_talk2.mp4"),
 ("B_snackpouch", f"{T}/talk_B_snackpouch.mp4"),
 ("I_confess",    f"{T}/talk_I_confess.mp4"),
 ("B_colorgame",  f"{T}/talk_B_colorgame.mp4"),
 ("B_button",     f"{T}/talk_B_button.mp4"),
 ("I_gathering",  f"{T}/talk_I_gathering.mp4"),
 ("B_ants",       f"{T}/talk_B_ants.mp4"),
]
scaled = []
for i,(lab,p) in enumerate(CLIPS):
    if not os.path.exists(p):
        print(f"  MISSING {lab}: {p}"); continue
    o = f"{TMP}/{i:02d}.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",p,"-vf",
        "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1",
        "-r","24","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-ar","44100","-b:a","192k",o], check=True)
    scaled.append(o); print(f"  {lab} ok")
listf = f"{TMP}/list.txt"
open(listf,"w").write("\n".join(f"file '{s}'" for s in scaled))
OUT = f"{T}/EP2_DIALOGUE_REEL.mp4"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",listf,"-c","copy",OUT], check=True)
d = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",OUT]).decode().strip()
print(f"REEL: {float(d):.1f}s -> {OUT}")
