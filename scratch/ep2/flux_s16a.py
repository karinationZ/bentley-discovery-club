#!/usr/bin/env python3
"""Make s16a by EDITING the approved s16_exchange frame (single source of truth) — change ONLY Indi's colour
(red-fawn patches, color-game), preserve the EXACT style/render/proportions/composition. FLUX Kontext (conservative),
input hosted on tmpfiles. Run: KIE_KEY=... python3 scratch/ep2/flux_s16a.py
"""
import os, json, time, urllib.request, subprocess
KEY = os.environ["KIE_KEY"]
GEN = "https://api.kie.ai/api/v1/flux/kontext/generate"
REC = "https://api.kie.ai/api/v1/flux/kontext/record-info?taskId={}"
SRC = "/project/scratch/ep2/hero_v2/s16_exchange.png"
OUT = "/project/scratch/ep2/hero_v2/s16a_colorgame.png"

PROMPT = ("Keep this entire image EXACTLY the same — the dog, the composition, the lighting, the 3D rendering style, the "
          "proportions, and the octopus's face, eyes, shape and size. Make ONLY ONE change: the small purple octopus is "
          "playfully mimicking her friend, so add soft patches of warm RED-FAWN / coral-orange colour blooming across her "
          "purple skin (a partial colour-change). Change nothing else.")

def host_tmpfiles(p):
    out = subprocess.check_output(["curl","-s","-F",f"file=@{p}","https://tmpfiles.org/api/v1/upload"]).decode()
    url = json.loads(out)["data"]["url"]
    return url.replace("http://","https://").replace("tmpfiles.org/","tmpfiles.org/dl/")

def post(body):
    req = urllib.request.Request(GEN, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type":"application/json"})
    return json.load(urllib.request.urlopen(req))
def get(url):
    for i in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}"})))
        except Exception as e:
            print(f"   poll retry {i+1}: {str(e)[:55]}"); time.sleep(4)
    return None
def dl(url, path):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})) as r, open(path,"wb") as f:
        f.write(r.read())

def credits():
    d = get("https://api.kie.ai/api/v1/chat/credit"); return d["data"] if d else "?"

print("bal before:", credits())
done = None
for whole in range(3):
    turl = host_tmpfiles(SRC); print("tmpfiles:", turl)
    r = post({"prompt": PROMPT, "inputImage": turl, "model":"flux-kontext-max", "aspectRatio":"16:9", "outputFormat":"png"})
    tid = r["data"]["taskId"]; print("taskId:", tid)
    t0 = time.time()
    while time.time()-t0 < 200:
        d = get(REC.format(tid))
        if not d: continue
        sf = d.get("data",{}).get("successFlag")
        if sf == 1: done = d["data"]["response"]["resultImageUrl"]; break
        if sf in (2,3): print("FLUX gen failed:", d["data"].get("errorMessage")); break
        time.sleep(4)
    if done: break
    print("retrying..."); time.sleep(6)
if done:
    dl(done, OUT); print("DONE ->", OUT)
else:
    print("FLUX FAILED")
print("bal after:", credits())
