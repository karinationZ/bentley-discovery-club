#!/usr/bin/env python3
"""QA one synced line: dense frame sweep + color-drift check vs keyframe.
Usage: qa_line.py <LABEL>  -> scratch/omni_ep3/out/<LABEL>.qa.png + drift metrics"""
import sys, subprocess, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path("/project")
label=sys.argv[1]
mp4=ROOT/f"scratch/omni_ep3/out/{label}.mp4"; key=ROOT/f"scratch/omni_ep3/keys/{label}.png"
dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(mp4)]).decode())
ts=[round(0.05+i*(dur-0.2)/11,2) for i in range(12)]
kimg=np.asarray(Image.open(key).convert("RGB").resize((320,180)),dtype=float)
tiles=[]; drifts=[]
for t in ts:
    f=f"/tmp/qa_{label}_{t}.png"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(t),"-i",str(mp4),"-frames:v","1",f])
    im=Image.open(f).convert("RGB")
    arr=np.asarray(im.resize((320,180)),dtype=float)
    drift=float(np.abs(arr-kimg).mean())   # mean abs RGB diff vs keyframe (motion+color)
    drifts.append(drift)
    tt=im.resize((320,180)); d=ImageDraw.Draw(tt)
    d.rectangle([0,0,150,18],fill=(0,0,0)); d.text((4,2),f"{t}s d={drift:.0f}",fill=(255,255,0)); tiles.append(tt)
cols=4; rows=(len(tiles)+cols-1)//cols
g=Image.new("RGB",(320*cols,180*rows),(15,15,15))
for i,t2 in enumerate(tiles): g.paste(t2,((i%cols)*320,(i//cols)*180))
qa=ROOT/f"scratch/omni_ep3/out/{label}.qa.png"; g.save(qa)
print(f"{label}: dur {dur:.2f}s  drift mean {np.mean(drifts):.1f} max {np.max(drifts):.1f} (vs keyframe; <25 good, >40 = investigate)")
print(f"QA sheet -> {qa}")
