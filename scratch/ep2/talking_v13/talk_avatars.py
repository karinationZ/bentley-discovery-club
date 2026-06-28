#!/usr/bin/env python3
"""EP2 v13 talking pass — Phase 2: Kling-Avatar each Bentley line from its expression face-CU keyframe,
then grade. Line audio = scratch/ep2/restart_v3/vo/labels/<LINE>.mp3 (clean Bentley-only).
Run: set -a;source .env;set +a
  python3 talk_avatars.py wave1          # 6 verification lines (one per expression)
  python3 talk_avatars.py rest           # the remaining 37
  python3 talk_avatars.py P4_B04 P6_B09  # specific lines
"""
import sys, subprocess, concurrent.futures
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

KEYS_DIR = ROOT / "scratch/ep2/talking_v13/keys"
LBL = ROOT / "scratch/ep2/restart_v3/vo/labels"
OUT = ROOT / "scratch/ep2/talking_v13/avatars"; OUT.mkdir(parents=True, exist_ok=True)

KEY = {  # approved picks
    "curious": "key_curious_0.png", "delighted": "key_delighted_0.png", "reassuring": "key_reassuring_1.png",
    "playful": "key_playful_1.png", "calm": "key_calm_1.png", "awe": "key_awe_0.png",
}
MAP = {  # every Bentley line -> expression
    "P1_B01": "playful", "P1_B02": "awe", "P1_B03": "curious", "P1_B04": "delighted", "P1_B05": "delighted",
    "P1_B06": "curious", "P1_B07": "curious",
    "P2_B01": "curious", "P2_B02": "awe", "P2_B03": "playful", "P2_B04": "awe", "P2_B05": "curious", "P2_B06": "playful",
    "P3_B01": "curious", "P3_B02": "awe", "P3_B03": "delighted", "P3_B04": "playful", "P3_B05": "curious",
    "P4_B01": "delighted", "P4_B02": "delighted", "P4_B03": "playful", "P4_B04": "curious", "P4_B05": "playful",
    "P4_B06": "delighted", "P4_B07": "delighted", "P4_B08": "playful",
    "P5_B01": "playful", "P5_B02": "curious", "P5_B03": "calm", "P5_B04": "curious", "P5_B05": "playful",
    "P5_B06": "delighted", "P5_B07": "delighted", "P5_B08": "curious",
    "P6_B01": "delighted", "P6_B02": "awe", "P6_B03": "awe", "P6_B04": "calm", "P6_B05": "curious",
    "P6_B06": "awe", "P6_B07": "curious", "P6_B08": "playful", "P6_B09": "delighted",
}
TONE = {
    "curious": "with bright curious energy and a gentle head-tilt, eyes sparkling",
    "delighted": "with delighted joyful energy, eyes shining with happiness",
    "reassuring": "warmly and gently, soft loving reassuring eyes, calm and tender",
    "playful": "with playful cheeky energy, bright and fun",
    "calm": "calmly and present, gentle attentive eyes",
    "awe": "with wide-eyed wonder and surprise",
}
GRADE = ("eq=brightness=0.05:saturation=1.14:contrast=1.05,unsharp=3:3:0.4:3:3:0.0,format=yuv420p")

WAVE1 = ["P1_B03", "P4_B07", "P6_B04", "P1_B01", "P4_B04", "P2_B02"]  # one per expression


def prompt_for(expr):
    return (f"Bentley the red-fawn Boxer puppy speaks straight to camera {TONE[expr]}; soft natural small-dog mouth "
            "movements in time with her words, ears floppy down, no human teeth, no human grin. Bright daylight on her "
            "face. Keep her exact look, do not redraw her.")


def worker(line):
    expr = MAP[line]; key = KEYS_DIR / KEY[expr]; aud = LBL / f"{line}.mp3"
    if not key.exists() or not aud.exists():
        return {"line": line, "err": f"missing {'key' if not key.exists() else 'audio'}"}
    try:
        r = kie_client.run("kling/ai-avatar-standard",
                           {"image_url": catbox_host(str(key)), "audio_url": catbox_host(str(aud)), "prompt": prompt_for(expr)},
                           timeout=1200, poll=10)
        raw = OUT / f"{line}_raw.mp4"; kie_client.download(r["urls"][0], str(raw))
        grd = OUT / f"{line}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf", GRADE,
                        "-c:v", "libx264", "-crf", "18", "-c:a", "copy", str(grd)], check=True)
        return {"line": line, "expr": expr, "cr": r.get("credits"), "out": str(grd)}
    except Exception as e:
        return {"line": line, "err": str(e)[:160]}


def main(lines):
    print(f"bal before: {kie_client.credits()} | rendering {len(lines)} lines", flush=True)
    spent = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for d in ex.map(worker, lines):
            if d.get("err"):
                print(f"  FAIL {d['line']}: {d['err']}", flush=True)
            else:
                spent += d.get("cr") or 0
                print(f"  OK {d['line']} ({d['expr']}) {d.get('cr')}cr", flush=True)
    print(f"bal after: {kie_client.credits()} | batch credits ~{spent}", flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["wave1"]:
        lines = WAVE1
    elif a == ["rest"]:
        done = {p.stem for p in OUT.glob("*.mp4") if not p.stem.endswith("_raw")}
        lines = [l for l in MAP if l not in done]
    elif a == ["all"]:
        lines = list(MAP)
    else:
        lines = a
    main(lines)
