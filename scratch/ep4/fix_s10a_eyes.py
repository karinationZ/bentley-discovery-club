#!/usr/bin/env python3
"""s10a eye fix (owner 2026-07-05: 'Eyes are too cartoonish, too googly eyes').
Per locked law: surgical edit on an otherwise-approved frame = FLUX Kontext (max), minimal change.
Input: kf_batch_master/s10a_worm_c1.png (approved staging: the delighted double-take).
FLUX gotcha: host input on tmpfiles (FLUX fetcher can't pull catbox/KIE-CDN URLs)."""
import os, sys, json, time, subprocess, urllib.request

KEY = os.environ["KIE_KEY"]
GEN = "https://api.kie.ai/api/v1/flux/kontext/generate"
REC = "https://api.kie.ai/api/v1/flux/kontext/record-info?taskId={}"
SRC = "/project/scratch/ep4/kf_batch_master/s10a_worm_c1.png"
OUT = "/project/scratch/ep4/kf_batch_master/s10a_worm_c1_eyefix.png"

PROMPT = ("Fix ONLY the puppy's eyes: replace the huge round white googly cartoon eyeballs with "
          "normal-sized natural puppy eyes — warm BROWN irises filling most of each eye, modest white "
          "only at the corners, natural eyelids, keeping her surprised delighted expression (raised "
          "brows, open mouth stay as they are). The eyes must look like a real Boxer puppy's brown "
          "eyes, gentle and dimensional, NOT enlarged, NOT googly, NOT cartoon circles. Keep her face "
          "structure, black mask, fur, body, pose, the butterfly, the chrysalis and the entire rest of "
          "the image EXACTLY the same.")

def tmpfiles_host(path):
    out = subprocess.check_output(["curl", "-s", "-F", f"file=@{path}",
                                   "https://tmpfiles.org/api/v1/upload"]).decode()
    url = json.loads(out)["data"]["url"]
    return url.replace("tmpfiles.org/", "tmpfiles.org/dl/")

def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))

def get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))

def main():
    src_url = tmpfiles_host(SRC)
    print("hosted:", src_url, flush=True)
    r = post(GEN, {"prompt": PROMPT, "inputImage": src_url, "model": "flux-kontext-max",
                   "aspectRatio": "16:9", "outputFormat": "png"})
    tid = r["data"]["taskId"]; print("taskId:", tid, flush=True)
    t0 = time.time()
    while time.time() - t0 < 240:
        d = get(REC.format(tid))["data"]
        flag = d.get("successFlag")
        if flag == 1:
            url = d["response"]["resultImageUrl"]
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp, open(OUT, "wb") as f:
                f.write(resp.read())
            print("EYEFIX DONE ->", OUT, flush=True); return
        if flag in (2, 3):
            raise RuntimeError(f"flux fail (flag {flag})")
        time.sleep(6)
    raise TimeoutError(tid)

if __name__ == "__main__":
    main()
