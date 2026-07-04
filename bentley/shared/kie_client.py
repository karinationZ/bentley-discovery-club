#!/usr/bin/env python3
"""Minimal kie.ai jobs client — createTask + poll recordInfo. Returns result URLs + credits + secs.
Auth: KIE_KEY env. Models: google/nano-banana, google/nano-banana-edit, kling-2.6/image-to-video.
Video models are gated by bentley/shared/gates.py (Animatic Lock spend guard) — see its docstring."""
import os, json, time, urllib.request
KEY = os.environ["KIE_KEY"]
BASE = "https://api.kie.ai/api/v1/jobs"

try:
    from bentley.shared import gates as _gates
except ImportError:  # loaded standalone (importlib spec pattern used by scratch scripts)
    import importlib.util as _ilu
    _s = _ilu.spec_from_file_location("_gates", os.path.join(os.path.dirname(__file__), "gates.py"))
    _gates = _ilu.module_from_spec(_s); _s.loader.exec_module(_gates)

def _post(path, body):
    req = urllib.request.Request(f"{BASE}/{path}", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))

def _get(path):
    req = urllib.request.Request(f"{BASE}/{path}", headers={"Authorization": f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))

def run(model, inp, timeout=600, poll=5):
    _gates.assert_spend_allowed(model)  # video renders require a PASSED Animatic Lock (gates.py)
    r = _post("createTask", {"model": model, "input": inp})
    if r.get("code") != 200 or not r.get("data"):
        raise RuntimeError(f"kie createTask rejected ({r.get('code')}): {r.get('msg')}")
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
