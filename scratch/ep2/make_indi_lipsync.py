#!/usr/bin/env python3
"""Indi toothless lip-sync: amplitude-driven mouth-openness from the VO, composited from the toothless atlas.
No teeth possible (shapes are hand-made). Run: python3 scratch/ep2/make_indi_lipsync.py <vo.mp3> <out.mp4>
"""
import sys, os, wave, array, subprocess
from PIL import Image, ImageDraw, ImageFilter
ROOT = "/project"
ATLAS = f"{ROOT}/scratch/ep2/atlas"
TMP = f"{ROOT}/scratch/ep2/talking/_lsf"; os.makedirs(TMP, exist_ok=True)
VO = sys.argv[1] if len(sys.argv) > 1 else f"{ROOT}/scratch/ep2/vo/I_hide.mp3"
OUTV = sys.argv[2] if len(sys.argv) > 2 else f"{ROOT}/scratch/ep2/talking/_indi_lipsync_test.mp4"
FPS = 24
OUTW, OUTH = 1920, 1080
MOUTH_BOX = (0.27, 0.51, 0.42, 0.65)          # Indi mouth region (frac of frame)
TH = (0.12, 0.45)                              # RMS thresholds -> level 0/1/2 (closed/small/mid); wide dropped (soft speech)

# 1) amplitude envelope -> per-frame level
wav = f"{TMP}/vo.wav"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",VO,"-ac","1","-ar","44100","-sample_fmt","s16",wav], check=True)
w = wave.open(wav, "rb"); sr = w.getframerate(); n = w.getnframes(); raw = w.readframes(n); w.close()
samples = array.array("h"); samples.frombytes(raw)   # mono int16
dur = n / sr; nframes = int(dur * FPS) + 1; spf = sr // FPS
rms = []
for i in range(nframes):
    seg = samples[i*spf:(i+1)*spf]
    rms.append((sum(s*s for s in seg)/len(seg))**0.5 if len(seg) else 0)
peak = sorted(rms)[int(len(rms)*0.95)] or 1
norm = [min(1.0, r/peak) for r in rms]
# smooth (moving avg, window 3)
sm = [sum(norm[max(0,i-1):i+2])/len(norm[max(0,i-1):i+2]) for i in range(len(norm))]
levels = []
for v in sm:
    levels.append(0 if v < TH[0] else 1 if v < TH[1] else 2)
# min-hold 2 frames to avoid 1-frame flicker
for i in range(1, len(levels)-1):
    if levels[i] != levels[i-1] and levels[i] != levels[i+1]:
        levels[i] = levels[i-1]
print(f"dur {dur:.2f}s  {nframes} frames  level histogram:",
      {k: levels.count(k) for k in range(3)})

# 2) build canvas + mouth patches
base = Image.open(f"{ATLAS}/indi_closed.png").convert("RGB").resize((OUTW, OUTH))
x0,y0,x1,y1 = [int(MOUTH_BOX[0]*OUTW), int(MOUTH_BOX[1]*OUTH), int(MOUTH_BOX[2]*OUTW), int(MOUTH_BOX[3]*OUTH)]
pw,ph = x1-x0, y1-y0
mask = Image.new("L",(pw,ph),0); d=ImageDraw.Draw(mask)
ins=int(min(pw,ph)*0.18); d.rectangle([ins,ins,pw-ins,ph-ins],fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(ins*0.7))
patches = {}
for lvl,name in {1:"small",2:"mid"}.items():
    img = Image.open(f"{ATLAS}/indi_{name}.png").convert("RGB").resize((OUTW,OUTH))
    patches[lvl] = img.crop((x0,y0,x1,y1))

# 3) render frames
for f in os.listdir(TMP):
    if f.endswith(".png"): os.remove(os.path.join(TMP,f))
for i,lvl in enumerate(levels):
    fr = base.copy()
    if lvl > 0: fr.paste(patches[lvl], (x0,y0), mask)
    fr.save(f"{TMP}/f_{i:04d}.png")

# 4) encode + mux VO
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{TMP}/f_%04d.png",
                "-i",VO,"-c:v","libx264","-pix_fmt","yuv420p","-crf","16","-c:a","aac","-b:a","192k",
                "-shortest",OUTV], check=True)
print("DONE ->", OUTV)
