#!/usr/bin/env python3
"""Ep2 assemble v3 — P0 QA fixes: DE-LOOP (clips play ONCE, freeze last frame to fill VO, no loop resets);
trim talk-clip dead tails to audio length; FILL-FRAME (scale+crop, no letterbox bars); title OVERLAID on the
opening shot at 0:00 (no mid-episode teal card); chase line restored (B_chase+B_rude); end-card catchphrase = Bentley VO;
heavier crop on the captioned catchphrase clip. Run: python3 scratch/ep2/assemble_ep2.py"""
import os, json, re, subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT = "/project"
W, H, FPS = 1280, 720, 24
AUD = ["-ar","48000","-ac","2"]
VO = f"{ROOT}/scratch/ep2/vo"; NEWMO = f"{ROOT}/assets/pilot_shots/ep2/motion"; TALK = f"{ROOT}/scratch/ep2/talking"
ASM = f"{ROOT}/scratch/ep2/assembly"; SEG = f"{ASM}/segs"; os.makedirs(SEG, exist_ok=True)
PLATE = f"{ROOT}/assets/character_design/TidePool_plate.jpg"
AWE = f"{ROOT}/scratch/ep2/motion/bentley_cu_awe_motion.mp4"

def durof(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode().strip())
def audur(p):
    try: return float(subprocess.check_output(["ffprobe","-v","error","-select_streams","a:0","-show_entries","stream=duration","-of","csv=p=0",p]).decode().strip())
    except Exception: return durof(p)
def speech_end(p):
    """Where speech actually ends = start of the TRAILING silence (a silence_start with no matching
    silence_end runs to clip end). Avatar clips embed a long silent tail; trimming to audio length
    keeps it. Returns None if speech runs to the end (no trailing silence)."""
    try:
        out = subprocess.run(["ffmpeg","-i",p,"-af","silencedetect=n=-38dB:d=0.8","-f","null","-"],
                             capture_output=True,text=True).stderr
        starts = re.findall(r"silence_start: ([0-9.]+)", out); ends = re.findall(r"silence_end: ([0-9.]+)", out)
        if starts and len(starts) > len(ends): return float(starts[-1])
    except Exception: pass
    return None

CROP = {"a3_14_stoplook": 0.74, "a5_31_button": 0.74}   # heavier crop kills burned-in captions; others default
SRCMAP = {"a3_15_settle": "a3_15b_calm.mp4"}   # de-dup: the 0:53 settle uses its OWN self-calming clip, not the reintro clip
OVR = {
 "a0_04_ink_reaction": {"kind":"voover","video":AWE,"vo":f"{VO}/B_hook2.mp3"},
 "a1_06_reintro": {"kind":"voover","video":f"{NEWMO}/a3_15_settle.mp4","vo":f"{VO}/N_intro.mp3"},
 "a1_07_chase": {"kind":"voover","video":f"{NEWMO}/a1_07_chase.mp4","vo":f"{VO}/B_chase.mp3"},
 "a1_08_camo": {"kind":"voover","video":f"{NEWMO}/a1_08_camo.mp4","vo":f"{VO}/N_camo.mp3"},
 "a4_25_wedged": {"kind":"voover","video":f"{NEWMO}/a4_25_wedged.mp4","vo":f"{VO}/I_hurt.mp3"},
 "a4_28_squeeze": {"kind":"voover","video":f"{ROOT}/scratch/ep2/motion/s20_squeeze_motion.mp4","vo":f"{VO}/N_boneless.mp3"},
 "a5_32_science": {"kind":"voover","video":f"{NEWMO}/a5_32_science.mp4","vo":f"{VO}/N_hearts.mp3"},  # de-duped: own 3-hearts clip (was a4_29_reform reuse)
 "a6_34_ants": {"kind":"voover","video":f"{NEWMO}/a6_34_ants.mp4","vo":f"{VO}/N_outro.mp3"},
 "a6_36_teasecard": {"kind":"card","text":"NEXT TIME","sub":"The Ant City Beneath Our Feet","dur":3},
 "a6_37_outro": {"kind":"card","text":"Subscribe for the next adventure","sub":"","dur":4,"vo":f"{VO}/B_stoplook.mp3"},
}
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"

def _title_png(out):
    img = Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
    try:
        f1=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",70)
        f2=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",34)
    except Exception: f1=f2=ImageFont.load_default()
    t="BENTLEY'S BIG ADVENTURES"; s="The Octopus Escape Artist"
    tw=d.textlength(t,font=f1); sw=d.textlength(s,font=f2)
    d.text(((W-tw)/2,H*0.40),t,fill=(255,222,120,255),font=f1,stroke_width=5,stroke_fill=(20,12,0,235))
    d.text(((W-sw)/2,H*0.55),s,fill=(250,252,255,255),font=f2,stroke_width=3,stroke_fill=(0,8,18,225))
    img.save(out)

def title_establish(out, dur=4.0):
    tp=f"{ASM}/_title.png"; _title_png(tp)
    live=f"{NEWMO}/plate_live.mp4"
    if os.path.exists(live):                                       # LIVE photoreal water (not a static still)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",live,"-loop","1","-i",tp,"-f","lavfi","-i","anullsrc=r=48000:cl=stereo",
            "-t",f"{dur:.2f}","-filter_complex",
            f"[0:v]{FILL},eq=brightness=-0.02:saturation=1.06,fade=t=in:st=0:d=0.4[bg];"
            f"[1:v]format=rgba,fade=t=in:st=0.4:d=0.7:alpha=1,fade=t=out:st={max(0,dur-0.9):.2f}:d=0.8:alpha=1[t];[bg][t]overlay,format=yuv420p[v]",
            "-map","[v]","-map","2:a","-c:v","libx264","-c:a","aac","-b:a","192k"]+AUD+[out],check=True)
        return
    subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-i",PLATE,"-loop","1","-i",tp,"-f","lavfi","-i","anullsrc=r=48000:cl=stereo",
        "-t",f"{dur:.2f}","-filter_complex",
        f"[0:v]scale={2*W}:{2*H},zoompan=z='min(zoom+0.0018,1.18)':d={int(dur*FPS)}:x='iw/2-(iw/zoom/2)+sin(in/22)*40':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},eq=brightness=-0.05[bg];"
        f"[1:v]format=rgba,fade=t=in:st=0.2:d=0.6:alpha=1,fade=t=out:st={max(0,dur-0.8):.2f}:d=0.7:alpha=1[t];[bg][t]overlay,format=yuv420p[v]",
        "-map","[v]","-map","2:a","-c:v","libx264","-c:a","aac","-b:a","192k"]+AUD+[out],check=True)

def make_card(text, sub, dur, out, vo=None):
    img=Image.new("RGB",(W,H),(12,28,40)); d=ImageDraw.Draw(img)
    try:
        f1=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",64)
        f2=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",34)
    except Exception: f1=f2=ImageFont.load_default()
    tw=d.textlength(text,font=f1); d.text(((W-tw)/2,H*(0.40 if sub else 0.46)),text,fill=(255,220,120),font=f1)
    if sub: sw=d.textlength(sub,font=f2); d.text(((W-sw)/2,H*0.56),sub,fill=(230,235,240),font=f2)
    p=out.replace(".mp4",".png"); img.save(p)
    cmd=["ffmpeg","-y","-loglevel","error","-loop","1","-i",p]
    cmd += (["-i",vo] if vo else ["-f","lavfi","-i","anullsrc=r=48000:cl=stereo"])
    cmd += ["-t",str(dur),"-r",str(FPS),"-vf",f"scale={W}:{H},format=yuv420p","-af","apad",
            "-map","0:v","-map","1:a","-c:v","libx264","-c:a","aac","-b:a","192k"]+AUD+[out]
    subprocess.run(cmd, check=True)

def seg_fill(video, dur, out, crop_frac=None, vo=None, hold=False):
    vf=[]
    if crop_frac: vf.append(f"crop=iw:ih*{crop_frac}:0:0")
    vf.append(FILL)
    if hold: vf.append(f"tpad=stop_mode=clone:stop_duration={dur:.2f}")
    cmd=["ffmpeg","-y","-loglevel","error"]
    is_img=video.lower().endswith((".jpg",".png"))
    cmd += (["-loop","1","-i",video] if is_img else ["-i",video])
    cmd += (["-i",vo] if vo else ["-f","lavfi","-i","anullsrc=r=48000:cl=stereo"])
    cmd += ["-t",f"{dur:.2f}","-r",str(FPS),"-vf",",".join(vf),"-af","apad","-map","0:v","-map","1:a",
            "-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-c:a","aac","-b:a","192k"]+AUD+[out]
    subprocess.run(cmd, check=True)

SL = json.load(open(f"{ROOT}/episodes/ep2/shotlists/ep2_master.json"))["shots"]
segs=[]
for i,s in enumerate(SL):
    sid=s["id"]; out=f"{SEG}/{i:02d}_{sid}.mp4"; o=OVR.get(sid)
    if sid=="a0_05_title": continue                                # title now overlaid on the opening shot
    if sid=="a0_01_establish": title_establish(out, 4.0)           # TITLE at 0:00 over the opening shot
    elif o and o["kind"]=="card": make_card(o["text"],o["sub"],o["dur"],out,vo=o.get("vo"))
    elif o and o["kind"]=="voover":
        dur=max(durof(o["video"]),durof(o["vo"])); seg_fill(o["video"],dur,out,vo=o["vo"],hold=True)  # play once + hold, no loop
    elif s["type"]=="talk":
        src=s.get("src") or f"{TALK}/talk_{'B' if s.get('voice')=='bentley' else 'I'}_{sid.split('_')[-1]}.mp4"
        se=speech_end(src); ad=min((se+0.4) if se else audur(src)+0.3, durof(src))  # trim to actual speech-end (kills avatar's silent tail)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",src,"-t",f"{ad:.2f}","-vf",
            (f"crop=iw:ih*{CROP.get(sid,0.87)}:0:0,{FILL},format=yuv420p"),"-r",str(FPS),
            "-c:v","libx264","-crf","18","-c:a","aac","-b:a","192k"]+AUD+[out],check=True)
    else:
        src=(f"{NEWMO}/{SRCMAP[sid]}" if sid in SRCMAP else None) or s.get("src") or f"{NEWMO}/{sid}.mp4"
        if not os.path.exists(src): print(f"  SKIP {sid}"); continue
        seg_fill(src, min(durof(src), float(s.get("dur",durof(src)))), out)
    segs.append(out); print(f"  {i:02d} {sid}: {durof(out):.1f}s", flush=True)

# ---- P0-C: per-shot colour normalization toward the uniform profile (V57 / S32, neutral daylight) ----
import numpy as np
GRADE_EXEMPT={"a0_01_establish","a6_36_teasecard","a6_37_outro","a1_08_camo","a3_23_colorchange","a3_24_youdidme"}
GRADE_TGTV={"a2_12_eelstir":38,"a2_11_bolt":48}   # mood shots stay intentionally darker (parseable, not flat)
def normalize_seg(path,sid):
    if sid in GRADE_EXEMPT: return
    tV=GRADE_TGTV.get(sid,57); tS=32; d=durof(path); fr=path[:-4]+"_probe.png"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",f"{d/2:.2f}","-i",path,"-frames:v","1","-vf","scale=240:-1",fr],check=True)
    im=np.asarray(Image.open(fr).convert("HSV")).astype(float); os.remove(fr)
    V=im[...,2].mean()/255*100; S=im[...,1].mean()/255*100
    db=max(-0.16,min(0.16,(tV-V)/100*0.85)); ms=max(0.78,min(1.45,(tS/max(S,1.0))**0.6))
    if abs(db)<0.02 and 0.94<ms<1.06: return
    tmp=path[:-4]+"_n.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",path,"-vf",f"eq=brightness={db:.3f}:saturation={ms:.3f}",
                    "-c:v","libx264","-crf","18","-pix_fmt","yuv420p","-c:a","copy",tmp],check=True)
    os.replace(tmp,path)
print("  [grade] normalizing every shot toward V57/S32 ...", flush=True)
for s in segs: normalize_seg(s, os.path.basename(s)[3:-4])

listf=f"{ASM}/_list.txt"; open(listf,"w").write("\n".join(f"file '{s}'" for s in segs))
OUTV=f"{ASM}/EP2_v3.mp4"
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",listf,
                "-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-c:a","aac","-b:a","192k"]+AUD+[OUTV],check=True)
print(f"v3 PICTURE+DIALOGUE: {durof(OUTV):.1f}s -> {OUTV}", flush=True)
