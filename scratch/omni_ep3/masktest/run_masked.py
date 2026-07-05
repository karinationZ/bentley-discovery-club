#!/usr/bin/env python3
"""Reusable masked two-shot sync: run_masked.py <key.png> <mask.png> <audio.mp3> <outname> <prompt>
OmniHuman confines the performance to the masked speaker; listener stays still. Backoff on 50430."""
import os, sys, json, time, subprocess
from pathlib import Path
ROOT=Path("/project"); sys.path.insert(0,str(ROOT))
from bentley.shared import kie_client
KEY=os.environ["KIE_KEY"]; OUT=ROOT/"scratch/omni_ep3/masktest"
key,mask,aud,outname,prompt=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]
assert len(prompt)<=300, f"prompt {len(prompt)} chars > 300"
def up(p,n):
    r=subprocess.run(["curl","-s","-X","POST","https://kieai.redpandaai.co/api/file-stream-upload",
        "-H",f"Authorization: Bearer {KEY}","-F",f"file=@{p}","-F","uploadPath=bentley/masktest","-F",f"fileName={n}"],
        capture_output=True,text=True); d=json.loads(r.stdout); assert d.get("success"),d; return d["data"]["downloadUrl"]
img=up(key,f"{outname}_k.png"); au=up(aud,f"{outname}_a.mp3"); msk=up(mask,f"{outname}_m.png")
inp={"image_url":img,"audio_url":au,"mask_url":[msk],"prompt":prompt,"output_resolution":"720","pe_fast_mode":False,"seed":11}
ok=False
for attempt in range(15):
    r=kie_client._post("createTask",{"model":"omnihuman-1-5","input":inp}); assert r.get("code")==200,r
    tid=r["data"]["taskId"]; (OUT/f"{outname}.taskid").write_text(tid); print(f"{outname} taskId {tid} (try {attempt+1})",flush=True)
    t0=time.time(); st=None; d=None
    while time.time()-t0<1500:
        d=kie_client._get(f"recordInfo?taskId={tid}")["data"]; st=d.get("state")
        if st=="success":
            u=json.loads(d["resultJson"])["resultUrls"][0]; kie_client.download(u,str(OUT/f"{outname}.mp4"))
            print(f"{outname}: OK {d.get('creditsConsumed')}cr -> {outname}.mp4",flush=True); ok=True; break
        if st in ("fail","failed"): print(f"{outname}: FAIL {d.get('failCode')} {d.get('failMsg')}",flush=True); break
        time.sleep(15)
    if ok: break
    if st in ("fail","failed") and "50430" in str(d.get("failCode")): print("busy 50430 — 90s",flush=True); time.sleep(90); continue
    break
