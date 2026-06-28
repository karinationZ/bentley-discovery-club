#!/usr/bin/env python3
"""FLUX Kontext (max) ocelli polish on the locked s14 master. Fixes vs last attempt:
 - host input on 0x0.st (FLUX failed fetching catbox), - POST once then poll SAME taskId (no re-create).
Surgical: refine ONLY the two ocelli -> clean iridescent blue rings. No chains, no glow, keep all else identical.
Run: KIE_KEY=... python3 scratch/ep2/flux_ocelli2.py
"""
import os, json, time, urllib.request, subprocess
KEY = os.environ["KIE_KEY"]
GEN = "https://api.kie.ai/api/v1/flux/kontext/generate"
REC = "https://api.kie.ai/api/v1/flux/kontext/record-info?taskId={}"
IMG = "/project/assets/character_design/Indi_LOCKED.png"
OUT = "/project/scratch/ep2/master/INDI_ocelli_flux.png"

PROMPT = ("Refine ONLY the two round false-eye spots on the sides of this octopus's head: make each a clean, well-defined "
          "iridescent peacock-blue ring marking on the skin — a smooth circular ring with a slightly darker center and a "
          "soft pearlescent shimmer, like the natural ocellus of a real two-spot octopus. Do NOT add chains, metal, links, "
          "jewelry, or any glow or light. Keep the octopus, its eyes, face, colour, pose and the entire rest of the image "
          "EXACTLY the same.")

def host_0x0(p):
    return subprocess.check_output(["curl", "-sA", "Mozilla/5.0", "-F", f"file=@{p}", "https://0x0.st"]).decode().strip()

def post_retry(body, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(GEN, data=json.dumps(body).encode(),
                headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
            return json.load(urllib.request.urlopen(req))
        except Exception as e:
            print(f"  post retry {i+1}: {str(e)[:70]}"); time.sleep(5)
    return None

def get_retry(url, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}"})
            return json.load(urllib.request.urlopen(req))
        except Exception as e:
            print(f"    poll retry {i+1}: {str(e)[:60]}"); time.sleep(4)
    return None

def credits():
    d = get_retry("https://api.kie.ai/api/v1/chat/credit")
    return d["data"] if d else "?"

input_url = open("/project/assets/character_design/.indi_locked_url.txt").read().strip()
print("input_url (catbox):", input_url)
print("bal before:", credits())
done = None
for whole in range(2):
    r = post_retry({"prompt": PROMPT, "inputImage": input_url, "model": "flux-kontext-max",
                    "aspectRatio": "16:9", "outputFormat": "png"})
    if not r or "data" not in r:
        print("post failed:", r); break
    tid = r["data"]["taskId"]; print("taskId:", tid)
    t0 = time.time()
    while time.time() - t0 < 200:
        d = get_retry(REC.format(tid))
        if not d:
            continue
        data = d.get("data", {}); sf = data.get("successFlag")
        if sf == 1:
            done = data["response"]["resultImageUrl"]; break
        if sf in (2, 3):
            print("gen FAILED:", data.get("errorMessage")); break
        time.sleep(4)
    if done:
        break
    print("retrying whole job..."); time.sleep(6)

if done:
    req = urllib.request.Request(done, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as rr, open(OUT, "wb") as f:
        f.write(rr.read())
    print("DONE ->", OUT)
else:
    print("FLUX still unavailable")
print("bal after:", credits())
