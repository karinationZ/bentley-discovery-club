#!/usr/bin/env python3
"""Recover any completed FLUX Kontext tasks (poll record-info with CONNECTION retry, don't re-create).
Also report KIE balance to assess spend."""
import os, json, time, urllib.request
KEY = os.environ["KIE_KEY"]
REC = "https://api.kie.ai/api/v1/flux/kontext/record-info?taskId={}"
TIDS = [
    "fluxkontext_2819c39cac254a4ba7f57cd71a34682c",
    "fluxkontext_3fabde624102427384b8d1750b7033e5",
    "fluxkontext_9c6f04fd033c4474966e00f85c8b95e7",
    "fluxkontext_25493e0c8c2f4085a0d0769171865e12",
]
OUT = "/project/scratch/ep2/master/INDI_flux_ocelli.png"

def get(url, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}"})
            return json.load(urllib.request.urlopen(req))
        except Exception as e:
            print(f"   poll retry {i+1}: {str(e)[:70]}"); time.sleep(4)
    return None

def credits():
    r = get("https://api.kie.ai/api/v1/chat/credit")
    return r["data"] if r else "?"

def dl(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r, open(path, "wb") as f:
        f.write(r.read())

print("KIE credits now:", credits())
got = None
for tid in TIDS:
    d = get(REC.format(tid))
    if not d:
        print(tid[:28], "-> no response"); continue
    data = d.get("data", {})
    sf = data.get("successFlag")
    print(tid[:28], "-> successFlag:", sf, "| err:", data.get("errorMessage"))
    if sf == 1 and not got:
        got = data["response"]["resultImageUrl"]
if got:
    dl(got, OUT); print("recovered ->", OUT)
else:
    print("no completed task to recover")
