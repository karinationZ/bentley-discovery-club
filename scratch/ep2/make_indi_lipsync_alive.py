#!/usr/bin/env python3
"""ALIVE Indi lip-sync v2 — SMOOTH: attack/release envelope follower + cross-faded toothless mouth shapes.
Fixes too-fast/abrupt motion (no per-frame snapping). Run: python3 make_indi_lipsync_alive.py <vo.mp3> <out.mp4>"""
import sys, os, wave, array, subprocess, json
from PIL import Image, ImageDraw, ImageFilter
ROOT = "/project"
ATLAS = f"{ROOT}/scratch/ep2/atlas"
CANVAS = f"{ROOT}/scratch/ep2/talking/_indi_canvas.mp4"
VO = sys.argv[1] if len(sys.argv) > 1 else f"{ROOT}/scratch/ep2/vo/I_hide.mp3"
OUTV = sys.argv[2] if len(sys.argv) > 2 else f"{ROOT}/scratch/ep2/talking/_indi_lipsync_alive.mp4"
CF = f"{ROOT}/scratch/ep2/talking/_cf"; OF = f"{ROOT}/scratch/ep2/talking/_of"
for d in (CF, OF): os.makedirs(d, exist_ok=True)
FPS = 24
MOUTH_BOX = (0.27, 0.51, 0.42, 0.65)
# --- tuning (natural mouth motion) ---
PRESMOOTH = 2        # envelope moving-avg half-window (window = 2*N+1)
ATT, REL  = 0.16, 0.10   # max openness change per frame: opens a bit faster than it closes
FLOOR     = 0.09     # below this, mouth fully at rest (closed)
GAMMA     = 1.35     # >1 -> mouth rests more, opens mainly on stressed syllables

# canvas dims + frames
info = json.loads(subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height","-of","json",CANVAS]).decode())["streams"][0]
W, H = info["width"], info["height"]
for f in os.listdir(CF):
    if f.endswith(".png"): os.remove(os.path.join(CF,f))
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",CANVAS,f"{CF}/c_%04d.png"], check=True)
cframes = sorted(os.listdir(CF)); print(f"canvas {W}x{H}, {len(cframes)} frames")

# amplitude envelope
wav = f"{ROOT}/scratch/ep2/talking/_lsf/vo.wav"; os.makedirs(os.path.dirname(wav), exist_ok=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",VO,"-ac","1","-ar","44100","-sample_fmt","s16",wav], check=True)
w = wave.open(wav,"rb"); sr=w.getframerate(); n=w.getnframes(); raw=w.readframes(n); w.close()
s = array.array("h"); s.frombytes(raw)
dur = n/sr; nframes = int(dur*FPS)+1; spf = sr//FPS
rms = [ (sum(x*x for x in s[i*spf:(i+1)*spf])/max(1,len(s[i*spf:(i+1)*spf])))**0.5 for i in range(nframes) ]
peak = sorted(rms)[int(len(rms)*0.95)] or 1
norm = [min(1.0, r/peak) for r in rms]
def mavg(a,k): return [sum(a[max(0,i-k):i+k+1])/len(a[max(0,i-k):i+k+1]) for i in range(len(a))]
env = mavg(norm, PRESMOOTH)
# attack/release follower -> eased openness
o = 0.0; foll = []
for t in env:
    o = min(t, o+ATT) if t > o else max(t, o-REL)
    foll.append(o)
openness = []
for v in foll:
    v = 0.0 if v < FLOOR else (v-FLOOR)/(1-FLOOR)
    openness.append(v**GAMMA)
print(f"dur {dur:.2f}s  open avg {sum(openness)/len(openness):.2f} max {max(openness):.2f}")

# toothless patches keyed by openness, cross-faded
x0,y0,x1,y1 = int(MOUTH_BOX[0]*W),int(MOUTH_BOX[1]*H),int(MOUTH_BOX[2]*W),int(MOUTH_BOX[3]*H)
pw,ph = x1-x0,y1-y0
mask = Image.new("L",(pw,ph),0); d=ImageDraw.Draw(mask)
ins=int(min(pw,ph)*0.18); d.rectangle([ins,ins,pw-ins,ph-ins],fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(ins*0.7))
KEYS = [(0.0,"closed"),(0.5,"small"),(1.0,"mid")]
kp = {k: Image.open(f"{ATLAS}/indi_{nm}.png").convert("RGB").resize((W,H)).crop((x0,y0,x1,y1)) for k,nm in KEYS}
kv = [k for k,_ in KEYS]

for f in os.listdir(OF):
    if f.endswith(".png"): os.remove(os.path.join(OF,f))
for i,o in enumerate(openness):
    im = Image.open(f"{CF}/{cframes[min(i,len(cframes)-1)]}").convert("RGB")
    if (W,H) != im.size: im = im.resize((W,H))
    oc = max(0.0, min(1.0, o))
    for j in range(len(kv)-1):
        if oc <= kv[j+1] or j == len(kv)-2:
            lo,hi = kv[j],kv[j+1]; frac = (oc-lo)/(hi-lo) if hi>lo else 0.0
            patch = Image.blend(kp[lo], kp[hi], max(0.0,min(1.0,frac))); break
    im.paste(patch,(x0,y0),mask)
    im.save(f"{OF}/o_{i:04d}.png")
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{OF}/o_%04d.png","-i",VO,
                "-c:v","libx264","-pix_fmt","yuv420p","-crf","16","-c:a","aac","-b:a","192k","-shortest",OUTV], check=True)
print("DONE ->", OUTV)
