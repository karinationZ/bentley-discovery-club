#!/usr/bin/env python3
"""COMPOSITE-LOCK a character's face: paste the clean KEYFRAME face onto every frame of a motion clip (feathered),
so the AI cannot add teeth/smiles. Works when the head stays ~still. Reassembles to mp4.
Usage hard-coded for the s22 test. Run: python3 scratch/ep2/composite_lock.py
"""
import os, subprocess, json
from PIL import Image, ImageDraw, ImageFilter
ROOT = "/project"
KF = f"{ROOT}/scratch/ep2/hero_v2/s22_pawhold.png"
CLIP = f"{ROOT}/scratch/ep2/motion/s22_pawhold_motion.mp4"
OUT = f"{ROOT}/scratch/ep2/motion/s22_locked.mp4"
FR = f"{ROOT}/scratch/ep2/motion/_lf"; os.makedirs(FR, exist_ok=True)
BOX = (0.165, 0.50, 0.47, 0.90)   # Indi head/face region (fractional), generous + feathered

# clip dims + fps
info = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
                       "stream=width,height,r_frame_rate","-of","json",CLIP],capture_output=True,text=True).stdout
st = json.loads(info)["streams"][0]; W,H = st["width"],st["height"]
num,den = st["r_frame_rate"].split("/"); fps = float(num)/float(den)
print("clip", W,H,"fps",round(fps,2))

# clean face patch from keyframe (resized to clip dims)
kf = Image.open(KF).convert("RGB").resize((W,H))
x0,y0,x1,y1 = [int(BOX[0]*W),int(BOX[1]*H),int(BOX[2]*W),int(BOX[3]*H)]
patch = kf.crop((x0,y0,x1,y1)); pw,ph = patch.size
# feathered mask
m = Image.new("L",(pw,ph),0); d=ImageDraw.Draw(m)
inset = int(min(pw,ph)*0.16)
d.rectangle([inset,inset,pw-inset,ph-inset],fill=255)
m = m.filter(ImageFilter.GaussianBlur(inset*0.7))

# extract frames
for f in os.listdir(FR):
    os.remove(os.path.join(FR,f))
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",CLIP,f"{FR}/f_%04d.png"],check=True)
frames = sorted(os.listdir(FR))
for fn in frames:
    fp = f"{FR}/{fn}"; im = Image.open(fp).convert("RGB")
    im.paste(patch,(x0,y0),m)
    im.save(fp)
print("composited", len(frames),"frames")

subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",f"{fps}","-i",f"{FR}/f_%04d.png",
                "-c:v","libx264","-pix_fmt","yuv420p","-crf","16",OUT],check=True)
print("DONE ->", OUT)
