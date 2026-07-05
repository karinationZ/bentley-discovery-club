#!/usr/bin/env python3
"""SYNC-MATCH QA — the detector my motion-sweep was missing. Wrong-speaker asks 'who moves';
this asks 'does the moving mouth match the WORDS'. Per dialogue beat: correlate the audio speech
envelope (loud=talking) with the on-screen mouth-band motion. High corr = synced; ~0 = flapping to
nothing (VO-over). Validates against known beats (synced CUs should score high, raw plates low).
Run: python3 scratch/ep3/qa_syncmatch.py"""
import importlib.util, subprocess, io
from pathlib import Path
import numpy as np
ROOT = Path("/project")
spec = importlib.util.spec_from_file_location("bs", ROOT / "episodes/ep3/build_sections.py")
bs = importlib.util.module_from_spec(spec); spec.loader.exec_module(bs)
FPS = 8

def dur(f):
    try: return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(f)]))
    except: return 0.0

def audio_env(mp3, n):
    """RMS speech envelope of the VO, resampled to n frames."""
    raw = subprocess.run(["ffmpeg","-v","error","-i",str(mp3),"-ac","1","-ar","16000","-f","f32le","-"],
                         capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.float32)
    if len(a) < 10: return np.zeros(n)
    win = np.array_split(a, n)
    env = np.array([np.sqrt((w**2).mean()) if len(w) else 0.0 for w in win])
    return env

def mouth_motion(clip, off, length, n):
    """Frame-to-frame motion in the lower-center 'mouth band', resampled to n frames."""
    tmp = Path("/tmp/_sm"); tmp.mkdir(exist_ok=True)
    for f in tmp.glob("*.png"): f.unlink()
    subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{off:.2f}","-t",f"{length:.2f}","-i",str(clip),
                    "-vf",f"fps={FPS},scale=320:-2","-an",str(tmp/"f_%03d.png")], check=True)
    fr = sorted(tmp.glob("f_*.png"))
    if len(fr) < 3: return np.zeros(n)
    from PIL import Image
    arr = [np.asarray(Image.open(f).convert("L"), dtype=np.int16) for f in fr]
    H, W = arr[0].shape
    band = slice(int(0.45*H), int(0.85*H)), slice(int(0.25*W), int(0.75*W))  # mouth-ish region
    mot = np.array([np.abs(b[band]-a[band]).mean() for a,b in zip(arr, arr[1:])])
    if len(mot) < 2: return np.zeros(n)
    # resample to n
    idx = np.linspace(0, len(mot)-1, n)
    return np.interp(idx, np.arange(len(mot)), mot)

def corr(a, b):
    if a.std() < 1e-6 or b.std() < 1e-6: return 0.0
    return float(np.corrcoef(a, b)[0,1])

# beat -> dominant on-screen clip + window (reuse assembler timing)
TAIL = 0.3
def beats():
    for sid, voice, vos, seq in bs.SECTIONS:
        vds = [dur(ROOT/f"episodes/ep3/vo/{l}.mp3") for l in vos]
        vd = sum(vds); length = max(vd,1.6)+TAIL
        lip = sum(float(p["dur"]) for p in seq if p.get("lipsync"))
        nonlip = sum(float(p["dur"]) for p in seq if not p.get("lipsync")) or 1.0
        avail = max(0.6, length-lip); t=0; wins=[]
        for p in seq:
            d = float(p["dur"]) if p.get("lipsync") else avail*(float(p["dur"])/nonlip)
            wins.append((t, t+d, p["src"], p.get("lipsync"))); t+=d
        lt = 0
        for l, ld in zip(vos, vds):
            if l.startswith("N_"): lt+=ld; continue
            s, e = lt, lt+ld; lt+=ld; mid=(s+e)/2
            cur = [(ws,we,src,lp) for ws,we,src,lp in wins if ws<=mid<we] or [wins[-1]]
            ws,we,src,lp = cur[0]
            if src in ("TITLE","CARD") or not (ROOT/src).exists(): continue
            yield l, sid, src, lp, max(0.1, mid-ws), min(ld, we-ws)

rows=[]
for l, sid, src, lp, off, wlen in beats():
    n = max(6, int(wlen*FPS))
    env = audio_env(ROOT/f"episodes/ep3/vo/{l}.mp3", n)
    mot = mouth_motion(ROOT/src, off, wlen, n)
    c = corr(env, mot)
    rows.append((c, l, sid, src.split("/")[-2] if "/" in src else src, bool(lp)))
rows.sort()
print(f"{'corr':>6}  {'line':14}{'synced?':8} plate")
print("-"*54)
for c,l,sid,plate,lp in rows:
    flag = "" if c>0.25 else ("  <-- FLAP (no sync)" if not lp else "  <-- SYNCED beat LOW?!")
    print(f"{c:6.2f}  {l:14}{'SYNC' if lp else 'vo-over':8} {plate}{flag}")
synced=[c for c,_,_,_,lp in rows if lp]; vo=[c for c,_,_,_,lp in rows if not lp]
print(f"\nmean corr  synced={np.mean(synced):.2f}  vo-over={np.mean(vo):.2f}  (detector works if synced >> vo-over)")
