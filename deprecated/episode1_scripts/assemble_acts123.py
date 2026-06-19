#!/usr/bin/env python3
"""Assemble Acts 1-3 master — drift-proof per-segment method.
Each shot -> normalized 1920x1080/24fps segment. Talk shots mux their CLEAN VO at
frame 0, video trimmed to min(clip, VO+TAIL) so the mouth never flaps past the line
and audio never drifts. Motion shots get a silent bed (music/ambient added in finish).
Then copy-concat -> ACTS123_1080_v1.mp4."""
import os, subprocess

ROOT  = "/home/user/src/youtube"
WORK  = f"{ROOT}/assets/pilot_shots/hybrid_ep1/acts123"
SEG   = f"{WORK}/segments"; os.makedirs(SEG, exist_ok=True)
PIPVO = f"{ROOT}/assets/pilot_shots/opening_movement/audio"
TAIL  = 0.18
NORM  = ("scale=1920:1080:force_original_aspect_ratio=decrease,"
         "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p")

# (id, type, vo_path|None)
SHOTS = [
  ("a1_01_shell",          "motion", None),
  ("a1_02_bentley_hear",   "talk",   f"{WORK}/a1_02_bentley_hear_vo.mp3"),
  ("a1_03_tracking",       "motion", None),
  ("a1_04_reveal",         "motion", None),
  ("a1_05_pip_meet",       "talk",   f"{PIPVO}/P_meet.wav"),
  ("a1_06_twoshot",        "talk",   f"{WORK}/a1_06_twoshot_vo.mp3"),
  ("a2_01_pip_correct",    "talk",   f"{PIPVO}/P_correct.wav"),
  ("a2_02_softbody",       "talk",   f"{PIPVO}/P_fact.wav"),
  ("a3_01_bentley_fix",    "talk",   f"{WORK}/a3_01_bentley_fix_vo.mp3"),
  ("a3_02_pip_flip",       "talk",   f"{PIPVO}/P_flip.wav"),
  ("a3_03_recoil",         "motion", None),
  ("a3_04_bentley_stunned","talk",   f"{WORK}/a3_04_bentley_stunned_vo.mp3"),
]
VENC = ["-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
        "-r","24","-video_track_timescale","12288"]
AENC = ["-c:a","aac","-b:a","192k","-ar","48000","-ac","2"]

def dur(p):
    return float(subprocess.check_output(
        ["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).strip())

segs, t = [], 0.0
print("shot                   type   start   seg")
for sid, typ, vo in SHOTS:
    clip = f"{WORK}/{sid}.mp4"; out = f"{SEG}/{sid}_seg.mp4"; cd = dur(clip)
    if typ == "motion":
        sd = cd
        cmd = ["ffmpeg","-y","-loglevel","error","-i",clip,
               "-f","lavfi","-t",f"{sd:.3f}","-i","anullsrc=channel_layout=stereo:sample_rate=48000",
               "-filter_complex", f"[0:v]{NORM},trim=0:{sd:.3f},setpts=PTS-STARTPTS[v]",
               "-map","[v]","-map","1:a"] + VENC + AENC + ["-t",f"{sd:.3f}",out]
    else:
        vd = dur(vo); sd = min(cd, vd + TAIL)
        cmd = ["ffmpeg","-y","-loglevel","error","-i",clip,"-i",vo,
               "-filter_complex",
                 f"[0:v]{NORM},trim=0:{sd:.3f},setpts=PTS-STARTPTS[v];"
                 f"[1:a]aresample=48000,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=0:{sd:.3f},asetpts=PTS-STARTPTS[a]",
               "-map","[v]","-map","[a]"] + VENC + AENC + ["-t",f"{sd:.3f}",out]
    subprocess.run(cmd, check=True)
    print(f"{sid:22s} {typ:6s} {t:6.2f} {sd:6.2f}")
    segs.append(out); t += sd

lst = f"{SEG}/concat.txt"
open(lst,"w").write("".join(f"file '{s}'\n" for s in segs))
master = f"{WORK}/ACTS123_1080_v1.mp4"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-c","copy",master], check=True)
print(f"\nMASTER -> {master}  total={dur(master):.2f}s")
