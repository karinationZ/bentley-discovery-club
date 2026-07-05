#!/usr/bin/env python3
"""Phase A refine — Tripo multiview_to_model (front/side/back from the turnaround). Quad+texture+PBR.
Slots: [front, left, back, right]; subject faces right -> side goes in the RIGHT slot, left empty."""
import os, json, time, sys, requests
from pathlib import Path
ROOT=Path("/project")
OUT=ROOT/"scratch/rig_build"; KEY=os.environ["TRIPO_API_KEY"]
H={"Authorization":f"Bearer {KEY}"}; BASE="https://api.tripo3d.ai/v2/openapi"
def upload(p):
    with open(p,"rb") as f:
        r=requests.post(f"{BASE}/upload",headers=H,files={"file":(p.name,f,"image/png")}).json()
    assert r.get("code")==0, r; return r["data"]["image_token"]
front=upload(OUT/"views/front.png"); side=upload(OUT/"views/side.png"); back=upload(OUT/"views/back.png")
print("uploaded 3 views",flush=True)
body={"type":"multiview_to_model",
      "files":[{"type":"png","file_token":front},{},{"type":"png","file_token":back},{"type":"png","file_token":side}],
      "texture":True,"pbr":True,"quad":True,"texture_quality":"standard"}
r=requests.post(f"{BASE}/task",headers={**H,"Content-Type":"application/json"},data=json.dumps(body)).json()
print("task-create:",json.dumps(r)[:300],flush=True)
if r.get("code")!=0: print("CREATE FAILED"); sys.exit(1)
tid=r["data"]["task_id"]; (OUT/"mv_taskid.txt").write_text(tid); print("task_id:",tid,flush=True)
t0=time.time()
while time.time()-t0<1200:
    d=requests.get(f"{BASE}/task/{tid}",headers=H).json()["data"]
    st=d.get("status"); print(f"  [{int(time.time()-t0)}s] {st} {d.get('progress')}%",flush=True)
    if st=="success":
        out=d.get("output",{}); print("OUTPUT:",json.dumps(out)[:300],flush=True)
        for key,fn in [("pbr_model","bentley_mv.fbx"),("model","bentley_mv_model.glb"),("rendered_image","mv_preview.webp")]:
            u=out.get(key); u=u.get("url") if isinstance(u,dict) else u
            if u: (OUT/fn).write_bytes(requests.get(u).content); print(f"  saved {fn}",flush=True)
        break
    if st in ("failed","cancelled","banned","expired","unknown"): print("FAILED",json.dumps(d)[:300],flush=True); break
    time.sleep(10)
print("balance after:",requests.get(f"{BASE}/user/balance",headers=H).json().get("data"),flush=True)
# chain turntable when the fbx lands
fbx=OUT/"bentley_mv.fbx"
if fbx.exists():
    import subprocess
    (OUT/"turntable_mv").mkdir(exist_ok=True)
    subprocess.run(["/opt/homebrew/bin/blender","--background","--python",str(OUT/"turntable.py"),
                    "--",str(fbx),str(OUT/"turntable_mv"),"12"],capture_output=True)
    print("TURNTABLE_MV_DONE",flush=True)
