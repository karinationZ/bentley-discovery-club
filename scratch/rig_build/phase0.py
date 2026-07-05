#!/usr/bin/env python3
"""PHASE 0 (0 credits): for every character line in the v9 EDL, compute which plate it plays over
(mirrors assemble_v2 VO-fill timing), audio duration, cost @720p, and extract the plate frame at the
line's midpoint for the GENERATE/WAIVE judgment sheet."""
import sys, subprocess, json
from pathlib import Path
ROOT=Path("/project"); sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"episodes/ep3"))
import importlib.util
spec=importlib.util.spec_from_file_location("bs",ROOT/"episodes/ep3/build_sections.py")
bs=importlib.util.module_from_spec(spec); spec.loader.exec_module(bs)
TAIL=0.3
def dur(f):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(f)]).decode())
rows=[]
for sid,voice,vos,seq in bs.SECTIONS:
    if not vos: continue
    vds=[dur(ROOT/f"episodes/ep3/vo/{l}.mp3") for l in vos]
    vd=sum(vds)
    length=max(vd,1.6)+TAIL
    lip=sum(float(p["dur"]) for p in seq if p.get("lipsync"))
    nonlip=sum(float(p["dur"]) for p in seq if not p.get("lipsync")) or 1.0
    avail=max(0.6,length-lip)
    # piece windows
    t=0.0; wins=[]
    for p in seq:
        d=float(p["dur"]) if p.get("lipsync") else avail*(float(p["dur"])/nonlip)
        wins.append((t,t+d,p["src"])); t+=d
    # line windows
    lt=0.0
    for label,ld in zip(vos,vds):
        if label.startswith("N_") or label=="B_promise":
            lt+=ld; continue
        s,e=lt,lt+ld; lt+=ld
        # overlapping pieces + dominant one
        ov=[(max(0,min(e,we)-max(s,ws)),src) for ws,we,src in wins if min(e,we)-max(s,ws)>0.15]
        ov.sort(reverse=True)
        main=ov[0][1] if ov else "?"
        rows.append({"section":sid,"line":label,"dur":round(ld,2),"speaker":"bentley" if label.startswith("B_") else "marco",
                     "plate":main,"others":[o[1].split("/")[-2] if "/" in o[1] else o[1] for o in ov[1:]],
                     "mid":round((s+e)/2,2),"sec_start":round(s,2)})
# extract judgment frames at the line midpoint of the MAIN plate
out=ROOT/"scratch/omni_ep3"; out.mkdir(parents=True,exist_ok=True)
for r in rows:
    src=r["plate"]
    if src in ("TITLE","CARD") or src=="?": r["frame"]=None; continue
    f=ROOT/src
    if not f.exists(): r["frame"]=None; continue
    # take the frame within the piece at the line's mid (approx: middle of the plate clip)
    fp=out/f"{r['line']}.png"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss","2.0","-i",str(f),"-frames:v","1",str(fp)])
    r["frame"]=str(fp)
CR_PER_S=25.7  # measured: 108cr / 4.2s @720p
tot=0
for r in rows:
    r["credits"]=round(r["dur"]*CR_PER_S)
    tot+=r["credits"]
(out/"phase0.json").write_text(json.dumps(rows,indent=1))
print(f"{'line':14}{'dur':>5} {'cr':>4}  plate")
for r in rows:
    print(f"{r['line']:14}{r['dur']:>5} {r['credits']:>4}  {r['plate'].split('/')[-2] if '/' in r['plate'] else r['plate']}")
print(f"\nTOTAL if ALL generated: {tot} cr (~${tot*0.005:.2f}) — before waivers")
