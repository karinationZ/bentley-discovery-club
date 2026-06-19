#!/usr/bin/env python3
"""Verify ZERO voice overlaps before rendering. Computes every dialogue window (embedded, from the
talk shots) + every narration/cry window (same scheduler as mix_v2_final.py), checks all pairs."""
import os, json, subprocess
ROOT = "/home/user/src/youtube/assets/pilot_shots/hybrid_ep1"
V2 = f"{ROOT}/v2"; AUD, WORK = f"{V2}/audio", f"{V2}/work"
TLJSON = json.load(open(f"{WORK}/timeline2.json")); TL = {s["id"]: s for s in TLJSON}
def st(i): return TL[i]["start"]
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).strip())
picdur = dur(f"{WORK}/EP1_v2_picture.mp4")
def next_talk_start(after):
    c = [s["start"] for s in TLJSON if s["kind"] == "talk" and s["start"] > after + 0.05]
    return min(c) if c else picdur

# dialogue windows = talk shots (embedded audio physically fills the shot)
dia = [(s["id"], s["start"], round(s["start"] + s["dur"], 2)) for s in TLJSON if s["kind"] == "talk"]
# narration schedule — MUST match mix_v2_final.py exactly
NARR = [
 (f"{AUD}/THEO_INTRO1.mp3","I1_establish",0.4),(f"{AUD}/THEO_INTRO2.mp3","I2_hero",0.3),
 (f"{AUD}/THEO_FACT1.mp3","a1_04_reveal",0.6),
 (f"{AUD}/BENTOS_chain.mp3","a4_01_crowd",0.3),(f"{AUD}/THEO_FACT4.mp3","BR2_lineshuffle",0.3),
 (f"{AUD}/THEO_N16.mp3","a4_03_cascade",0.3),(f"{AUD}/BENTOS_octo.mp3","a6_01_octopus",0.6),
 (f"{AUD}/THEO_outro.mp3","END_card",0.5),
]
CRY = (f"{AUD}/PIPOS_help1.mp3", "a1_02_hear", -1.5, 1.0)
events = sorted([(st(a)+o, p) for p,a,o in NARR] + [(st(CRY[1])+CRY[2], CRY[0])], key=lambda e: e[0])
narr, last_end = [], -10.0
for desired, path in events:
    start = max(desired, last_end + 0.25); avail = next_talk_start(start) - 0.2 - start
    cap = min(dur(path), avail)
    if path == CRY[0]: cap = min(cap, CRY[3])
    if cap >= 0.8:
        narr.append((os.path.basename(path).replace(".mp3",""), round(start,2), round(start+cap,2))); last_end = start + cap
    else:
        print(f"  (skip {os.path.basename(path)} — only {avail:.2f}s)")

allv = sorted([(n,s,e,"DIA") for n,s,e in dia] + [(n,s,e,"NARR") for n,s,e in narr], key=lambda x: x[1])
print("\n=== VOICE TIMELINE ===")
for n,s,e,k in allv: print(f"  {s:7.2f} - {e:7.2f}  [{k:4s}] {n}")
ov = 0
for i in range(len(allv)):
    for j in range(i+1, len(allv)):
        a, b = allv[i], allv[j]
        inter = min(a[2], b[2]) - max(a[1], b[1])
        if inter > 0.05:
            print(f"  !! OVERLAP {inter:.2f}s: {a[3]}:{a[0]} [{a[1]}-{a[2]}] x {b[3]}:{b[0]} [{b[1]}-{b[2]}]"); ov += 1
print(f"\nVOICE OVERLAPS: {ov}  -> {'PASS (zero overlaps)' if ov == 0 else 'FAIL'}")
