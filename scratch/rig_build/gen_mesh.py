#!/usr/bin/env python3
"""Phase A — Tripo image_to_model on the locked Bentley master. Quad topology (rig-ready) + texture + PBR.
Persists task_id immediately; downloads GLB + Tripo's preview render."""
import os, json, time, sys
import requests
from pathlib import Path
ROOT=Path("/project")
OUT=ROOT/"scratch/rig_build"; OUT.mkdir(parents=True,exist_ok=True)
KEY=os.environ["TRIPO_API_KEY"]; H={"Authorization":f"Bearer {KEY}"}
BASE="https://api.tripo3d.ai/v2/openapi"
IMG=ROOT/"assets/character_design/Bentley_MASTER_pixar.png"

# 1) upload
with open(IMG,"rb") as f:
    up=requests.post(f"{BASE}/upload",headers=H,files={"file":("bentley.png",f,"image/png")}).json()
print("upload:",json.dumps(up)[:200],flush=True)
tok=up["data"]["image_token"]

# 2) create task — quad (rig-ready), textured, PBR
body={"type":"image_to_model","file":{"type":"png","file_token":tok},
      "texture":True,"pbr":True,"quad":True,"texture_quality":"standard"}
r=requests.post(f"{BASE}/task",headers={**H,"Content-Type":"application/json"},data=json.dumps(body)).json()
print("task-create:",json.dumps(r)[:300],flush=True)
if r.get("code")!=0:
    print("CREATE FAILED",flush=True); sys.exit(1)
tid=r["data"]["task_id"]; (OUT/"mesh_taskid.txt").write_text(tid)
print("task_id:",tid,flush=True)

# 3) poll
t0=time.time()
while time.time()-t0<1200:
    d=requests.get(f"{BASE}/task/{tid}",headers=H).json()["data"]
    st=d.get("status"); pr=d.get("progress")
    print(f"  [{int(time.time()-t0)}s] {st} {pr}%",flush=True)
    if st=="success":
        out=d.get("output",{}); print("OUTPUT:",json.dumps(out)[:400],flush=True)
        # download GLB (prefer pbr_model, else model) + preview render
        for key,fn in [("pbr_model","bentley_pbr.glb"),("model","bentley.glb"),("rendered_image","tripo_preview.webp")]:
            u=out.get(key)
            if isinstance(u,dict): u=u.get("url")
            if u:
                data=requests.get(u).content; (OUT/fn).write_bytes(data)
                print(f"  saved {fn} ({len(data)} bytes)",flush=True)
        break
    if st in ("failed","cancelled","banned","expired","unknown"):
        print("TASK FAILED:",json.dumps(d)[:400],flush=True); break
    time.sleep(10)
bal=requests.get(f"{BASE}/user/balance",headers=H).json()
print("balance after:",bal.get("data"),flush=True)
