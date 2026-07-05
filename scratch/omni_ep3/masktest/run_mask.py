#!/usr/bin/env python3
"""OmniHuman MASK smoke test: two-shot keyframe + Marco line + Marco mask -> does ONLY Marco talk
while Bentley stays still? Judged sound-off. ~50cr."""
import os, sys, json, time, subprocess
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
KEY = os.environ["KIE_KEY"]
MT = ROOT / "scratch/omni_ep3/masktest"

def up(p, name):
    r = subprocess.run(["curl", "-s", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload",
        "-H", f"Authorization: Bearer {KEY}", "-F", f"file=@{p}", "-F", "uploadPath=bentley/masktest",
        "-F", f"fileName={name}"], capture_output=True, text=True)
    d = json.loads(r.stdout); assert d.get("success"), d; return d["data"]["downloadUrl"]

img = up(MT / "key.png", "mtkey.png")
aud = up(ROOT / "episodes/ep3/vo/M_checkyou.mp3", "mtaud.mp3")
msk = up(MT / "marco_mask.png", "mtmask.png")
prompt = ("Only the small golden ant on the left talks: cheerful, mandibles moving to the words, tiny "
          "gestures. The brown Boxer puppy on the right stays completely still and silent, mouth closed, "
          "calmly watching. Keep both exact designs, insect mandibles no teeth, background unchanged.")
inp = {"image_url": img, "audio_url": aud, "mask_url": [msk], "prompt": prompt,
       "output_resolution": "720", "pe_fast_mode": False, "seed": 11}
r = kie_client._post("createTask", {"model": "omnihuman-1-5", "input": inp})
print("createTask:", r.get("code"), r.get("msg") or "")
assert r.get("code") == 200, r
tid = r["data"]["taskId"]; (MT / "taskid.txt").write_text(tid)
print("taskId", tid, flush=True)
t0 = time.time()
while time.time() - t0 < 1500:
    d = kie_client._get(f"recordInfo?taskId={tid}")["data"]; st = d.get("state")
    if st == "success":
        u = json.loads(d["resultJson"])["resultUrls"][0]
        kie_client.download(u, str(MT / "marco_mask_result.mp4"))
        print(f"OK {d.get('creditsConsumed')}cr -> marco_mask_result.mp4", flush=True); break
    if st in ("fail", "failed"):
        print(f"FAIL {d.get('failCode')} {d.get('failMsg')}", flush=True); break
    time.sleep(15)
