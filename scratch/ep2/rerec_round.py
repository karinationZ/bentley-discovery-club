#!/usr/bin/env python3
"""Re-record the 2 approved line rewrites (Bentley) into the labels dir + update vo_timing text/duration.
Run: set -a;source .env;set +a; python3 scratch/ep2/rerec_round.py"""
import sys, json, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.voices.dialogue import tts_bentley
LBL = f"{ROOT}/scratch/ep2/restart_v3/vo/labels"
NEW = {
    "P2_B05": "But how do I find you?",          # was "A clue!" (made no sense)
    "P4_B04": "See? I can really stop and look.",  # was the mid-episode catchphrase (illogical there)
}
for lab, txt in NEW.items():
    tts_bentley(txt, f"{LBL}/{lab}.mp3")
    print(f"  recorded {lab}: {txt!r}", flush=True)
tp = f"{ROOT}/scratch/ep2/restart_v3/vo/vo_timing.json"
d = json.load(open(tp))
for e in d["label_audio"]:
    if e["label"] in NEW:
        e["text"] = NEW[e["label"]]
        e["duration"] = round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", e["path"]]).decode()), 3)
        print(f"  timing {e['label']}: {e['duration']}s", flush=True)
json.dump(d, open(tp, "w"), indent=2)
print("done", flush=True)
