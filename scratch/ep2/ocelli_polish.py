#!/usr/bin/env python3
"""Ocelli polish on the locked s14 master. Try FLUX Kontext (input hosted on tmpfiles, since FLUX can't fetch catbox);
if FLUX can't fetch either, FALL BACK to nano-banana (catbox) with corrected wording (no 'chain-link', no 'glow').
Surgical: change ONLY the two ocelli -> clean iridescent blue rings; keep everything else identical.
Run: KIE_KEY=... python3 scratch/ep2/ocelli_polish.py
"""
import os, json, time, urllib.request, subprocess, sys
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
KEY = os.environ["KIE_KEY"]
IMG = f"{ROOT}/assets/character_design/Indi_LOCKED.png"
CATBOX = open(f"{ROOT}/assets/character_design/.indi_locked_url.txt").read().strip()
OUT = f"{ROOT}/scratch/ep2/master/INDI_ocelli_polish.png"
GEN = "https://api.kie.ai/api/v1/flux/kontext/generate"
REC = "https://api.kie.ai/api/v1/flux/kontext/record-info?taskId={}"

PROMPT_FLUX = ("On each side of this octopus's head, below and slightly behind each eye, add ONE clear, defined, iridescent "
  "peacock-blue RING marking — a smooth blue circle/ring on the purple skin with a slightly darker center and a soft "
  "pearlescent shimmer, like the two false-eye ocelli of a real two-spot octopus. Make them clearly visible but natural and "
  "tasteful. Do NOT add any chains, metal, links, jewelry, glow or light. Keep the octopus, its real teal eyes, face, colour, "
  "pose and the entire rest of the image EXACTLY the same.")
PROMPT_NB = ("Keep this octopus EXACTLY the same — same face, eyes, colour, pose, body and background. Change ONLY the two round "
  "false-eye spots on the sides of her head into clean, defined, soft iridescent peacock-blue RING markings (a smooth circle "
  "with a slightly darker center and subtle pearlescent shimmer), like a real two-spot octopus. Do NOT add any chains, metal, "
  "links, jewelry, glow or light. NEGATIVE: chains, chain-link, metal rings, jewelry, glowing, neon, emissive, light-up, flat "
  "dull stains, changing the octopus, different face, human eyes, eyebrows, nose, film grain, watermark.")

def host_tmpfiles(p):
    out = subprocess.check_output(["curl","-s","-F",f"file=@{p}","https://tmpfiles.org/api/v1/upload"]).decode()
    j = json.loads(out); url = j["data"]["url"]            # http://tmpfiles.org/NNNN/name
    return url.replace("http://","https://").replace("tmpfiles.org/","tmpfiles.org/dl/")

def post(body):
    req = urllib.request.Request(GEN, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type":"application/json"})
    return json.load(urllib.request.urlopen(req))
def get(url):
    for i in range(6):
        try:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}"})
            return json.load(urllib.request.urlopen(req))
        except Exception as e:
            print(f"    poll retry {i+1}: {str(e)[:55]}"); time.sleep(4)
    return None
def dl(url, path):
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req) as r, open(path,"wb") as f: f.write(r.read())

print("bal before:", kie_client.credits())
# --- Try FLUX via tmpfiles ---
flux_ok = False
try:
    turl = host_tmpfiles(IMG); print("tmpfiles url:", turl)
    r = post({"prompt": PROMPT_FLUX, "inputImage": turl, "model":"flux-kontext-max", "aspectRatio":"16:9", "outputFormat":"png"})
    tid = r["data"]["taskId"]; print("FLUX taskId:", tid)
    t0 = time.time()
    while time.time()-t0 < 200:
        d = get(REC.format(tid))
        if not d: continue
        sf = d.get("data",{}).get("successFlag")
        if sf == 1:
            dl(d["data"]["response"]["resultImageUrl"], OUT); print("FLUX DONE ->", OUT); flux_ok = True; break
        if sf in (2,3):
            print("FLUX gen failed:", d["data"].get("errorMessage")); break
        time.sleep(4)
except Exception as e:
    print("FLUX path error:", str(e)[:120])

# --- Fallback: nano-banana via catbox ---
if not flux_ok:
    print("falling back to nano-banana (catbox) with corrected wording...")
    for i in range(4):
        try:
            r = kie_client.run("google/nano-banana-edit",
                {"prompt": PROMPT_NB, "image_urls":[CATBOX], "image_size":"16:9", "output_format":"png"})
            kie_client.download(r["urls"][0], OUT); print(f"NB DONE ({r['credits']}cr) ->", OUT); break
        except Exception as e:
            print(f"  nb retry {i+1}: {str(e)[:70]}"); time.sleep(6)
print("bal after:", kie_client.credits())
