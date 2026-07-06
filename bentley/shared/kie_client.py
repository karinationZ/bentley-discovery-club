#!/usr/bin/env python3
"""Minimal kie.ai jobs client — createTask + poll recordInfo. Returns result URLs + credits + secs.
Auth: KIE_KEY env. Models: google/nano-banana, google/nano-banana-edit, kling-3.0/video (legacy kling-2.6).
Two mechanical guards fire before any spend: gates.py (Animatic-Lock spend guard — video needs a PASSED
gate) and drift_guard.py (character video must last-frame-pin, drift lever #3). See their docstrings."""
import os, json, time, urllib.request
KEY = os.environ["KIE_KEY"]
BASE = "https://api.kie.ai/api/v1/jobs"


def _load(name):
    """Import a bentley.shared sibling, tolerating the standalone importlib pattern scratch scripts use."""
    try:
        import importlib
        return importlib.import_module(f"bentley.shared.{name}")
    except ImportError:
        import importlib.util as _ilu
        s = _ilu.spec_from_file_location(f"_{name}", os.path.join(os.path.dirname(__file__), f"{name}.py"))
        m = _ilu.module_from_spec(s); s.loader.exec_module(m); return m


_gates = _load("gates")
_drift = _load("drift_guard")

def _post(path, body):
    req = urllib.request.Request(f"{BASE}/{path}", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))

def _get(path):
    req = urllib.request.Request(f"{BASE}/{path}", headers={"Authorization": f"Bearer {KEY}"})
    return json.load(urllib.request.urlopen(req))

def run(model, inp, timeout=600, poll=5):
    _gates.assert_spend_allowed(model)   # video renders require a PASSED Animatic Lock (gates.py)
    _drift.assert_pin_ok(model, inp)     # character video must last-frame-pin (drift_guard.py, lever #3)
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
