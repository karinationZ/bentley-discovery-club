#!/usr/bin/env python3
"""SWITCH MODEL -> FLUX.1 Kontext (max) on KIE. Surgical edit: refine ONLY the two ocelli on s14 (the liked look)
into clean natural iridescent blue ring-markings. No chains, no glow, keep everything else identical.
Run: KIE_KEY=... python3 scratch/ep2/flux_ocelli.py
"""
import os, json, time, urllib.request
KEY = os.environ["KIE_KEY"]
GEN = "https://api.kie.ai/api/v1/flux/kontext/generate"
REC = "https://api.kie.ai/api/v1/flux/kontext/record-info?taskId={}"
S14_URL = "https://files.catbox.moe/cretsx.png"   # s14_emergence (the liked look)
OUT = "/project/scratch/ep2/master/INDI_flux_ocelli.png"

PROMPT = ("Refine ONLY the two round false-eye spots on the sides of this octopus's head: make each a clean, well-defined "
          "iridescent peacock-blue ring marking on the skin — a simple smooth circular ring with a slightly darker center "
          "and a soft pearlescent shimmer, like the natural ocellus of a real two-spot octopus. Do NOT add chains, metal, "
          "links, jewelry, or any glow or light. Keep the octopus, its eyes, face, colour, pose and the whole rest of the "
          "image EXACTLY the same.")

def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))

def get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))

def dl(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r, open(path, "wb") as f:
        f.write(r.read())

def flux_edit(prompt, input_url, model="flux-kontext-max", ar="16:9", tries=4):
    for attempt in range(tries):
        try:
            r = post(GEN, {"prompt": prompt, "inputImage": input_url, "model": model,
                           "aspectRatio": ar, "outputFormat": "png"})
            tid = r["data"]["taskId"]; print("taskId:", tid)
            t0 = time.time()
            while time.time() - t0 < 180:
                d = get(REC.format(tid))["data"]
                sf = d.get("successFlag")
                if sf == 1:
                    return d["response"]["resultImageUrl"]
                if sf in (2, 3):
                    raise RuntimeError(f"flux fail: {d.get('errorCode')} {d.get('errorMessage')}")
                time.sleep(3)
            raise TimeoutError("flux poll timeout")
        except Exception as e:
            print(f"   attempt {attempt+1} failed: {str(e)[:90]}"); time.sleep(6)
    return None

print("editing via FLUX Kontext max...")
url = flux_edit(PROMPT, S14_URL)
if url:
    dl(url, OUT); print("DONE ->", OUT)
else:
    print("FAILED")
