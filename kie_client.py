#!/usr/bin/env python3
"""Minimal kie.ai jobs client — createTask + poll recordInfo. Returns result URLs + credits + secs.
Auth: KIE_KEY env. Models: google/nano-banana, google/nano-banana-edit, kling-2.6/image-to-video."""
import os, json, time, urllib.request
KEY = os.environ["KIE_KEY"]
BASE = "https://api.kie.ai/api/v1/jobs"

def _post(path, body):
    req = urllib.request.Request(f"{BASE}/{path}", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))

def _get(path):
    req = urllib.request.Request(f"{BASE}/{path}", headers={"Authorization": f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))

def run(model, inp, timeout=600, poll=5):
    r = _post("createTask", {"model": model, "input": inp})
    tid = r["data"]["taskId"]
    t0 = time.time()
    while time.time() - t0 < timeout:
        d = _get(f"recordInfo?taskId={tid}")["data"]
        st = d.get("state")
        if st == "success":
            urls = json.loads(d["resultJson"])["resultUrls"]
            return {"urls": urls, "credits": d.get("creditsConsumed"), "secs": round(time.time() - t0), "tid": tid}
        if st in ("fail", "failed"):
            raise RuntimeError(f"kie fail ({d.get('failCode')}): {d.get('failMsg')}")
        time.sleep(poll)
    raise TimeoutError(f"kie timeout on {tid}")

def credits():
    req = urllib.request.Request("https://api.kie.ai/api/v1/chat/credit", headers={"Authorization": f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))["data"]

def download(url, path):
    """kie's tempfile CDN 403s the default urllib UA — needs a browser UA."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r, open(path, "wb") as f:
        f.write(r.read())
    return path
