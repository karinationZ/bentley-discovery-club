#!/usr/bin/env python3
"""Poll the already-started Infinitalk Indi job, download, extract + zoom mouth frames for teeth QA."""
import os, json, time, urllib.request, subprocess
ROOT = "/project"
KEY = os.environ["KIE_KEY"]
TID = "a7ba50dbed515f3a8390662aa162546d"
OUT = f"{ROOT}/scratch/ep2/talking"
OUTV = f"{OUT}/_indi_infinitalk_test.mp4"

def get(path):
    req = urllib.request.Request(f"https://api.kie.ai/api/v1/jobs/{path}", headers={"Authorization": f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))

t0 = time.time(); url = None
while time.time() - t0 < 600:
    d = get(f"recordInfo?taskId={TID}")["data"]
    st = d.get("state")
    if st == "success":
        url = json.loads(d["resultJson"])["resultUrls"][0]
        print(f"SUCCESS {d.get('creditsConsumed')}cr in {round(time.time()-t0)}s"); break
    if st in ("fail", "failed"):
        print("FAIL:", d.get("failMsg")); break
    time.sleep(5)
if url:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r, open(OUTV, "wb") as f: f.write(r.read())
    print("downloaded ->", OUTV)
    res = subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
        "stream=width,height","-of","csv=p=0:s=x",OUTV]).decode().strip()
    print("resolution:", res)
    for t in ["0.6","1.5","2.5","3.5","4.5"]:
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",t,"-i",OUTV,"-frames:v","1",f"{OUT}/_iinf_{t}.png"], check=False)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",t,"-i",OUTV,"-frames:v","1","-vf",
                        "crop=iw*0.30:ih*0.28:iw*0.22:ih*0.40,scale=900:-1:flags=lanczos",f"{OUT}/_iinfz_{t}.png"], check=False)
    print("frames + zooms ready")
print("=== INFINITALK POLL DONE ===")
