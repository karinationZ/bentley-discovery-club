#!/usr/bin/env python3
"""EP1 v2 FINAL (v4 — SYNC FIX). NO slow-mo on action (motion = native speed; only the 2 title
cards get a gentle 1.20x). TALK shots use their OWN EMBEDDED Kling audio trimmed to mouth length
(mouth==voice by construction; no tpad, no re-pinned VO). 3 real b-roll shots added (intro + climax).
Outputs EP1_v2_picture.mp4 (with embedded dialogue) + timeline2.json."""
import os, subprocess, json
from bentley.shared.ffio import dur
from bentley.shared.paths import episode_assets
ROOT = str(episode_assets("hybrid_ep1"))
D = {"v2": f"{ROOT}/v2", "a123": f"{ROOT}/acts123", "a456": f"{ROOT}/acts456", "fix": f"{ROOT}/v2/fixed"}
WORK = f"{ROOT}/v2/work"; SEG = f"{WORK}/fseg"; os.makedirs(SEG, exist_ok=True)
TITLE = f"{WORK}/title_card.png"
NORM = ("scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24,format=yuv420p")
VENC = ["-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-r","24","-video_track_timescale","12288"]
AENC = ["-c:a","aac","-b:a","160k","-ar","48000","-ac","2"]

# id | src | dir | kind | dur(talk=embAud; motion ignored=native, except slowok cards) | opts
EDL = [
 # INTRO
 ("I1_establish","CLEAN_shell.mp4","v2","motion",6.05,{"title":True,"slowok":True}),
 ("I2_hero","INTRO2_hero.mp4","v2","motion",0,{}),
 ("BR3_explore","BR3_explore_NEW.mp4","fix","motion",0,{}),      # kie re-render: on-model short docked tail, fresh motion (kills loop-glitch)
 ("I3_listen","a1_03_tracking.mp4","a123","motion",0,{}),
 # BODY
 ("a1_02_hear","a1_02_react_NEW.mp4","fix","talk",4.00,{}),     # kie re-render: bright, no teeth, "A voice? Somebody needs help?"
 ("a1_04_reveal","a1_04_reveal.mp4","v2","motion",0,{}),
 ("a1_05_pip_meet","a1_05_pip_meet.mp4","v2","talk",6.90,{}),
 ("a1_06_twoshot","a1_06_twoshot.mp4","a123","talk",5.94,{}),
 ("N1_guess","N1_guess_NEW.mp4","fix","talk",7.20,{}),          # kie re-render: re-framed (tilt other way), teeth-clean, rapid-fire guesses
 ("a2_01_correct","a2_01_pip_correct.mp4","v2","talk",10.13,{}),
 ("a2_02_softbody","a2_02_softbody.mp4","v2","talk",11.47,{}),
 ("a3_01_fix","a3_01_bentley_fix.mp4","a123","talk",2.93,{}),
 ("a3_02a_wave","a3_02a_wave_NEW.mp4","fix","motion",0,{}),      # SPLIT: LIVE crashing wave (alive water); Pip VO seg1 over it (mix)
 ("a3_02b_pipcu","a3_02b_pipcu_NEW.mp4","fix","talk",15.40,{}), # SPLIT: dry Pip panic CU, lip-synced seg2 (no wave to freeze)
 ("a3_03_recoil","a3_03_recoil.mp4","v2","motion",0,{}),
 ("N3_bridge","N3_bridge_safe.mp4","v2","motion",0,{}),
 ("a3_04_stunned","a3_04_bentley_stunned.mp4","a123","talk",8.53,{}),
 ("N4_lonely","N4_pip_lonely.mp4","v2","talk",13.60,{}),
 ("N5_empathy","N5_bentley_empathy.mp4","v2","talk",10.36,{}),
 ("a4_01_crowd","a4_01_crowd.mp4","a456","motion",0,{}),
 ("BR2_lineshuffle","BR2_lineshuffle.mp4","v2","motion",0,{}),
 ("a4_02_lineup","a4_02_lineup.mp4","a456","motion",0,{}),
 ("a4_03_cascade","a4_03_cascade.mp4","a456","motion",0,{}),
 ("BR1_crableave","BR1_crableave.mp4","v2","motion",0,{}),
 ("a4_04_whoaa","a4_04_whoaa.mp4","a456","talk",5.70,{}),
 ("a5_01_piphome","a5_01_piphome.mp4","v2","motion",0,{}),
 ("a5_02_pipthanks","a5_02_pipthanks.mp4","v2","talk",14.13,{}),
 ("a5_03_disco","a5_03_disco.mp4","a456","talk",2.40,{"cropbottom":True}),
 ("N6_armor","N6_payoff_armor_NEW.mp4","fix","talk",9.86,{}),   # kie re-render: bright, soft mouth, "tiny knight in shiny armor"
 ("a5_04_tag","a5_04_tag_NEW.mp4","fix","talk",9.60,{}),        # kie re-render: bright charm CU, "Stop... Look... Listen..."
 ("a6_01_octopus","octopus_NEW.mp4","fix","motion",0,{}),        # kie re-render: dramatic tentacle wave + SPLASH, ~10s (was ~5s)
 ("END_card","CLEAN_shell.mp4","v2","motion",14.8,{"title":True,"slowok":True,"dim":True,"fo_st":12.8}),
]
# dur() imported from bentley.shared.ffio

segs, t, tl = [], 0.0, []
print(f"{'id':16s} {'kind':6s} {'start':>7s} {'dur':>6s} {'native':>7s}")
for sid, f, dd, kind, td, opt in EDL:
    src = f"{D[dd]}/{f}"; out = f"{SEG}/{sid}.mp4"; nd = dur(src)
    pre = ""
    if opt.get("cropbottom"): pre = "crop=iw:ih*0.90:0:0,"
    if opt.get("dim"): pre += "eq=brightness=-0.12:saturation=0.85,"
    if opt.get("bright"): pre += "eq=brightness=0.07:saturation=1.04:gamma=1.12,"
    if kind == "motion":
        tgt = td if opt.get("slowok") else nd          # native speed unless a title card
        slow = tgt > nd + 0.05
        vbase = f"{pre}setpts={tgt/nd:.4f}*PTS,{NORM}" if slow else f"{pre}{NORM}"
        vfilt = f"[0:v]{vbase},trim=0:{tgt:.3f},setpts=PTS-STARTPTS"
        if opt.get("title"):
            fo = opt.get("fo_st", 4.0)
            cmd = ["ffmpeg","-y","-loglevel","error","-i",src,"-loop","1","-i",TITLE,
                   "-f","lavfi","-t",f"{tgt:.3f}","-i","anullsrc=channel_layout=stereo:sample_rate=48000",
                   "-filter_complex",
                     f"{vfilt}[base];[1:v]format=rgba,fade=in:st=0.5:d=1.2:alpha=1,fade=out:st={fo}:d=1.0:alpha=1[tt];[base][tt]overlay=0:0[v]",
                   "-map","[v]","-map","2:a","-t",f"{tgt:.3f}"]+VENC+AENC+[out]
        else:
            cmd = ["ffmpeg","-y","-loglevel","error","-i",src,
                   "-f","lavfi","-t",f"{tgt:.3f}","-i","anullsrc=channel_layout=stereo:sample_rate=48000",
                   "-filter_complex", f"{vfilt}[v]",
                   "-map","[v]","-map","1:a","-t",f"{tgt:.3f}"]+VENC+AENC+[out]
    else:  # TALK — embedded Kling audio, trim to mouth length (embAud); NEVER tpad/slow
        tgt = min(td, nd)
        cmd = ["ffmpeg","-y","-loglevel","error","-i",src,
               "-filter_complex",
                 f"[0:v]{pre}{NORM},trim=0:{tgt:.3f},setpts=PTS-STARTPTS[v];"
                 f"[0:a]aresample=48000,atrim=0:{tgt:.3f},asetpts=PTS-STARTPTS,apad,atrim=0:{tgt:.3f}[a]",
               "-map","[v]","-map","[a]","-t",f"{tgt:.3f}"]+VENC+AENC+[out]
    subprocess.run(cmd, check=True)
    print(f"{sid:16s} {kind:6s} {t:7.2f} {tgt:6.2f} {nd:7.2f}")
    tl.append({"id": sid, "start": round(t,3), "dur": round(tgt,3), "kind": kind}); segs.append(out); t += tgt

lst = f"{SEG}/concat.txt"; open(lst,"w").write("".join(f"file '{s}'\n" for s in segs))
pic = f"{WORK}/EP1_v2_picture.mp4"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-c","copy",pic], check=True)
json.dump(tl, open(f"{WORK}/timeline2.json","w"), indent=1)
print(f"\nPICTURE -> {pic}  total={dur(pic):.2f}s ({dur(pic)/60:.2f} min)  [dialogue embedded]")
