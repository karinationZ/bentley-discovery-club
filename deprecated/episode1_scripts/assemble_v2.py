#!/usr/bin/env python3
"""EP1 v2 — STAGE 1: picture + synced dialogue backbone (27 shots, drift-proof per-segment).
Builds normalized 1920x1080/24fps segments (talk = clean VO muxed at frame 0, trimmed to
min(clip, VO+0.18); motion = silent, optional trim), concats -> EP1_v2_base_av.mp4.
Prints the shot timeline (start/dur) for Stage 2 (narration/music/SFX placement)."""
import os, subprocess, json
ROOT = "/project/assets/pilot_shots/ep1"
DIRS = {"v2": f"{ROOT}/v2", "acts123": f"{ROOT}/acts123", "acts456": f"{ROOT}/acts456"}
WORK = f"{ROOT}/v2/work"; SEG = f"{WORK}/seg"; os.makedirs(SEG, exist_ok=True)
TAIL = 0.18
NORM = ("scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p")
VENC = ["-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-r","24","-video_track_timescale","12288"]
AENC = ["-c:a","aac","-b:a","192k","-ar","48000","-ac","2"]

# (id, dir, type, trim_override|None)
SHOTS = [
 ("a1_01_shell","acts123","motion",5.0),
 ("a1_02_bentley_hear","acts123","talk",None),
 ("a1_03_tracking","acts123","motion",3.2),
 ("a1_04_reveal","v2","motion",None),
 ("a1_05_pip_meet","v2","talk",None),
 ("a1_06_twoshot","acts123","talk",None),
 ("N1_bentley_guess","v2","talk",None),
 ("a2_01_pip_correct","v2","talk",None),
 ("a2_02_softbody","v2","talk",None),
 ("N2_shell_science","v2","motion",None),
 ("a3_01_bentley_fix","acts123","talk",None),
 ("a3_02_pip_flip","v2","talk",None),
 ("a3_03_recoil","acts123","motion",None),
 ("N3_bridge_safe","v2","motion",None),
 ("a3_04_bentley_stunned","acts123","talk",None),
 ("N4_pip_lonely","v2","talk",None),
 ("N5_bentley_empathy","v2","talk",None),
 ("a4_01_crowd","acts456","motion",None),
 ("a4_02_lineup","acts456","motion",None),
 ("a4_03_cascade","acts456","motion",None),
 ("a4_04_whoaa","acts456","talk",None),
 ("a5_01_piphome","v2","motion",None),
 ("a5_02_pipthanks","v2","talk",None),
 ("a5_03_disco","acts456","talk",None),
 ("N6_payoff_armor","v2","talk",None),
 ("a5_04_tag","acts456","talk",None),
 ("a6_01_octopus","acts456","motion",None),
]
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).strip())

segs, t, timeline = [], 0.0, []
print(f"{'shot':24s} {'src':8s} {'type':6s} {'start':>7s} {'dur':>6s}")
for sid, d, typ, trim in SHOTS:
    clip = f"{DIRS[d]}/{sid}.mp4"; out = f"{SEG}/{sid}_seg.mp4"; cd = dur(clip)
    if typ == "motion":
        sd = trim if trim else cd
        cmd = ["ffmpeg","-y","-loglevel","error","-i",clip,
               "-f","lavfi","-t",f"{sd:.3f}","-i","anullsrc=channel_layout=stereo:sample_rate=48000",
               "-filter_complex", f"[0:v]{NORM},trim=0:{sd:.3f},setpts=PTS-STARTPTS[v]",
               "-map","[v]","-map","1:a"] + VENC + AENC + ["-t",f"{sd:.3f}",out]
    else:
        vo = f"{DIRS[d]}/{sid}_vo.mp3"; vd = dur(vo); sd = min(cd, vd + TAIL)
        if trim: sd = min(sd, trim)
        cmd = ["ffmpeg","-y","-loglevel","error","-i",clip,"-i",vo,
               "-filter_complex",
                 f"[0:v]{NORM},trim=0:{sd:.3f},setpts=PTS-STARTPTS[v];"
                 f"[1:a]aresample=48000,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=0:{sd:.3f},asetpts=PTS-STARTPTS[a]",
               "-map","[v]","-map","[a]"] + VENC + AENC + ["-t",f"{sd:.3f}",out]
    subprocess.run(cmd, check=True)
    print(f"{sid:24s} {d:8s} {typ:6s} {t:7.2f} {sd:6.2f}")
    timeline.append({"id": sid, "type": typ, "start": round(t,3), "dur": round(sd,3)})
    segs.append(out); t += sd

lst = f"{SEG}/concat.txt"; open(lst,"w").write("".join(f"file '{s}'\n" for s in segs))
base = f"{WORK}/EP1_v2_base_av.mp4"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-c","copy",base], check=True)
json.dump(timeline, open(f"{WORK}/timeline.json","w"), indent=1)
print(f"\nBASE A/V -> {base}  total={dur(base):.2f}s ({dur(base)/60:.2f} min)")
print(f"timeline -> {WORK}/timeline.json")
