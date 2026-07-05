import os, sys, json, time, subprocess
from pathlib import Path
ROOT=Path("/project"); sys.path.insert(0,str(ROOT))
from bentley.shared import kie_client
KEY=os.environ["KIE_KEY"]; MT=ROOT/"scratch/omni_ep3/masktest"
def up(p,n):
    r=subprocess.run(["curl","-s","-X","POST","https://kieai.redpandaai.co/api/file-stream-upload",
        "-H",f"Authorization: Bearer {KEY}","-F",f"file=@{p}","-F","uploadPath=bentley/masktest","-F",f"fileName={n}"],
        capture_output=True,text=True); d=json.loads(r.stdout); assert d.get("success"),d; return d["data"]["downloadUrl"]
img=up(MT/"key.png","shotkey.png"); aud=up(MT/"M_smellpath_test.mp3","shotaud.mp3"); msk=up(MT/"marco_mask.png","shotmask.png")
prompt=("Only the small ant on the left talks, warmly explaining, gesturing at the glowing trail, mandibles "
        "moving to the words. The brown Boxer puppy on the right stays still, mouth closed, listening. "
        "Keep exact designs, insect mandibles no teeth, background unchanged.")
inp={"image_url":img,"audio_url":aud,"mask_url":[msk],"prompt":prompt,"output_resolution":"720","pe_fast_mode":False,"seed":11}
ok=False
for attempt in range(15):                 # 50430 = concurrent/platform limit -> patient backoff
    r=kie_client._post("createTask",{"model":"omnihuman-1-5","input":inp})
    assert r.get("code")==200, r
    tid=r["data"]["taskId"]; (MT/"shot_taskid.txt").write_text(tid)
    print(f"taskId {tid} (attempt {attempt+1})",flush=True)
    t0=time.time(); st=None; d=None
    while time.time()-t0<1500:
        d=kie_client._get(f"recordInfo?taskId={tid}")["data"]; st=d.get("state")
        if st=="success":
            u=json.loads(d["resultJson"])["resultUrls"][0]; kie_client.download(u,str(MT/"SMELLPATH_masked.mp4"))
            print(f"OK {d.get('creditsConsumed')}cr -> SMELLPATH_masked.mp4",flush=True); ok=True; break
        if st in ("fail","failed"):
            print(f"FAIL {d.get('failCode')} {d.get('failMsg')}",flush=True); break
        time.sleep(15)
    if ok: break
    if st in ("fail","failed") and "50430" in str(d.get("failCode")):
        print("busy (50430) — backing off 90s",flush=True); time.sleep(90); continue
    break
