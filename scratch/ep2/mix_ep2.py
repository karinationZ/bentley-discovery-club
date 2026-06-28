#!/usr/bin/env python3
"""Ep2 final master — Stages 6-8: per-act MUSIC cues + key SFX + ambient bed over the v2 cut, upscaled to 1080p + graded.
Run: python3 scratch/ep2/mix_ep2.py"""
import os, subprocess
ROOT = "/project"
ASM = f"{ROOT}/scratch/ep2/assembly"; SEG = f"{ASM}/segs"
MUS = f"{ROOT}/assets/pilot_shots/ep1/v2/music"; SFX = f"{ROOT}/assets/pilot_shots/ep1/v2/sfx"
CUT = f"{ASM}/EP2_v3.mp4"; OUT = f"{ASM}/EP2_FINAL_v3.mp4"

def durof(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode().strip())

# 1) timeline: per-shot start + per-act duration, and shot-id -> start
segs = sorted(f for f in os.listdir(SEG) if f.endswith(".mp4"))
start = {}; act_dur = {}; t = 0.0
for f in segs:
    sid = f[3:-4]                                   # strip "NN_" and ".mp4"
    act = sid.split("_")[0]                          # a0..a6
    d = durof(f"{SEG}/{f}")
    start[sid] = t; act_dur[act] = act_dur.get(act, 0.0) + d; t += d
TOTAL = t
print(f"total {TOTAL:.1f}s; acts:", {k: round(v,1) for k,v in act_dur.items()})

# 2) per-act music cues, crossfaded, low
ACT_CUE = {"a0":"theme_wonder","a1":"theme_wonder","a2":"suspense","a3":"emotional_piano","a4":"suspense","a5":"emotional_piano","a6":"triumph"}
parts = []
for act in ["a0","a1","a2","a3","a4","a5","a6"]:
    if act not in act_dur: continue
    d = act_dur[act]; cue = f"{MUS}/{ACT_CUE[act]}.mp3"; o = f"{ASM}/_mus_{act}.wav"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-stream_loop","-1","-i",cue,"-t",f"{d:.2f}",
                    "-af",f"afade=t=in:st=0:d=0.8,afade=t=out:st={max(0,d-0.8):.2f}:d=0.8","-ar","48000","-ac","2",o],check=True)
    parts.append(o)
mlist = f"{ASM}/_muslist.txt"; open(mlist,"w").write("\n".join(f"file '{p}'" for p in parts))
MUSIC = f"{ASM}/_music.wav"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",mlist,"-ar","48000","-ac","2",MUSIC],check=True)

# 3) key SFX at shot starts (id, sfx, vol)
EV = [("a0_02_boop","chime",0.5),("a0_04_ink_reaction","octo_curl",0.5),("a1_07_chase","shake",0.45),
      ("a2_11_bolt","octo_curl",0.5),("a3_14_stoplook","sparkle",0.5),("a6_34_ants","skitter",0.45)]
EV = [(start[i], s, v) for i,s,v in EV if i in start and os.path.exists(f"{SFX}/{s}.mp3")]
SFXTRK = f"{ASM}/_sfx.wav"
if EV:
    cmd = ["ffmpeg","-y","-loglevel","error"]
    for _,s,_ in EV: cmd += ["-i",f"{SFX}/{s}.mp3"]
    fl = "".join(f"[{i}:a]adelay={int(t*1000)}|{int(t*1000)},volume={v}[s{i}];" for i,(t,_,v) in enumerate(EV))
    fl += "".join(f"[s{i}]" for i in range(len(EV))) + f"amix=inputs={len(EV)}:duration=longest:normalize=0,apad=whole_dur={TOTAL}[a]"
    subprocess.run(cmd + ["-filter_complex",fl,"-map","[a]","-t",f"{TOTAL:.2f}","-ar","48000","-ac","2",SFXTRK],check=True)

# 4) final: 1080p + grade + amix (dialogue + ambient + music + sfx)
amb = f"{SFX}/amb_ocean.mp3"
cmd = ["ffmpeg","-y","-loglevel","error","-i",CUT,"-stream_loop","-1","-i",amb,"-i",MUSIC]
amix_in = "[d][amb][mus]"; n = 3
if EV: cmd += ["-i",SFXTRK]; amix_in = "[d][amb][mus][sfx]"; n = 4
fc = ("[0:v]scale=1920:1080:flags=lanczos,eq=saturation=1.04:contrast=1.03[v];"  # per-shot normalize done in assembler; mild final polish only
      "[0:a]aresample=48000[d0];[d0]volume=1.0[d];[1:a]aresample=48000,volume=0.10[amb];[2:a]aresample=48000,volume=1.0[mus];"
      + ("[3:a]aresample=48000,volume=0.9[sfx];" if EV else "")
      + f"{amix_in}amix=inputs={n}:duration=first:normalize=0[a]")
cmd += ["-filter_complex",fc,"-map","[v]","-map","[a]","-c:v","libx264","-crf","18","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","192k","-ar","48000","-ac","2",OUT]
subprocess.run(cmd,check=True)
print(f"FINAL MASTER: {durof(OUT):.1f}s @1080p -> {OUT}")
