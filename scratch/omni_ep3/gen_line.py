#!/usr/bin/env python3
"""Generate ONE OmniHuman-synced line. Usage: gen_line.py <LABEL> <keyframe.png> <prompt> [seed]
Recipe: KIE-CDN upload, taskId persisted immediately, 720p, one attempt."""
import os, sys, json, time, subprocess
from pathlib import Path
ROOT=Path("/project")
label,key,prompt=sys.argv[1],sys.argv[2],sys.argv[3]
seed=int(sys.argv[4]) if len(sys.argv)>4 else 11
sys.path.insert(0,str(ROOT))
from bentley.shared import kie_client
KEY=os.environ["KIE_KEY"]; OUT=ROOT/"scratch/omni_ep3/out"; OUT.mkdir(parents=True,exist_ok=True)
def up(p,name):
    r=subprocess.run(["curl","-s","-X","POST","https://kieai.redpandaai.co/api/file-stream-upload",
        "-H",f"Authorization: Bearer {KEY}","-F",f"file=@{p}","-F","uploadPath=bentley/ep3sync","-F",f"fileName={name}"],
        capture_output=True,text=True)
    d=json.loads(r.stdout); assert d.get("success"), d; return d["data"]["downloadUrl"]
img=up(key,f"{label}.png"); aud=up(str(ROOT/f"episodes/ep3/vo/{label}.mp3"),f"{label}.mp3")
ok=False
for attempt in range(12):           # 50430 = busy slot/platform congestion -> patient backoff
    r=kie_client._post("createTask",{"model":"omnihuman-1-5","input":{"image_url":img,"audio_url":aud,
        "prompt":prompt,"output_resolution":"720","pe_fast_mode":False,"seed":seed}})
    assert r.get("code")==200, r
    tid=r["data"]["taskId"]; (OUT/f"{label}.taskid").write_text(tid)
    print(f"{label} taskId {tid} (attempt {attempt+1})",flush=True)
    t0=time.time(); st=None
    while time.time()-t0<1500:
        d=kie_client._get(f"recordInfo?taskId={tid}")["data"]; st=d.get("state")
        if st=="success":
            u=json.loads(d["resultJson"])["resultUrls"][0]
            kie_client.download(u,str(OUT/f"{label}.mp4"))
            print(f"{label}: OK {d.get('creditsConsumed')}cr",flush=True); ok=True; break
        if st in ("fail","failed"):
            print(f"{label}: FAIL {d.get('failCode')} {d.get('failMsg')}",flush=True); break
        time.sleep(15)
    if ok: break
    if st in ("fail","failed") and "50430" in str(d.get("failCode")):
        print(f"{label}: busy — backing off 90s",flush=True); time.sleep(90); continue
    break
