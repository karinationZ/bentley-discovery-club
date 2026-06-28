#!/usr/bin/env python3
"""EP2 v13 — selective Indi talking pass. Avatar her DIALOGUE lines (toothless prompt) from the Indi
expression keyframes; her camo/eel/escape/color-copy REVEAL lines are NOT here (they keep scene shots).
Run: set -a;source .env;set +a; python3 indi_avatars.py [all | wave1 | rest | <LINE>...]"""
import sys, subprocess, concurrent.futures
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

KEYS = ROOT / "scratch/ep2/talking_v13/indi_keys"
LBL = ROOT / "scratch/ep2/restart_v3/vo/labels"
OUT = ROOT / "scratch/ep2/talking_v13/indi_avatars"; OUT.mkdir(parents=True, exist_ok=True)

KEY = {"playful": "indi_playful.png", "proud": "indi_proud.png", "tender": "indi_tender.png"}
CU = {  # Indi DIALOGUE lines -> expression (reveal lines deliberately excluded)
    "P1_I01": "playful", "P1_I02": "playful", "P1_I03": "proud", "P1_I04": "playful", "P1_I05": "proud", "P1_I06": "playful",
    "P2_I04": "proud", "P2_I05": "playful", "P2_I06": "tender",
    "P3_I01": "playful", "P3_I04": "proud",
    "P4_I01": "playful", "P4_I02": "tender", "P4_I03": "playful", "P4_I04": "tender", "P4_I05": "tender",
    "P5_I01": "playful", "P5_I02": "playful", "P5_I03": "playful", "P5_I04": "playful", "P5_I05": "proud", "P5_I06": "playful", "P5_I08": "tender",
    "P6_I01": "proud", "P6_I02": "proud", "P6_I03": "playful", "P6_I04": "tender", "P6_I05": "playful", "P6_I08": "tender",
}
TONE = {"playful": "playfully and mischievously, a clever sparkle in her teal eyes",
        "proud": "proudly and confidently, bright teal eyes",
        "tender": "warmly and tenderly, soft sweet teal eyes"}
GRADE = "eq=brightness=0.05:saturation=1.12:contrast=1.04,unsharp=3:3:0.4:3:3:0.0,format=yuv420p"
WAVE1 = ["P4_I03", "P1_I03", "P6_I04"]  # one per expression


def prompt_for(expr):
    return (f"Indi the small purple octopus speaks {TONE[expr]}; her small soft TOOTHLESS mouth opens and closes softly in "
            "time with her words, gentle blinks, soft arms drifting. ABSOLUTELY NO teeth, NO gums, NO human mouth, NO human "
            "smile, NO human face. Keep her exact purple colour, teal eyes and two ring spots; do not redraw her.")


def worker(line):
    expr = CU[line]; key = KEYS / KEY[expr]; aud = LBL / f"{line}.mp3"
    if not key.exists() or not aud.exists():
        return {"line": line, "err": f"missing {'key:'+str(key) if not key.exists() else 'audio'}"}
    try:
        r = kie_client.run("kling/ai-avatar-standard",
                           {"image_url": catbox_host(str(key)), "audio_url": catbox_host(str(aud)), "prompt": prompt_for(expr)},
                           timeout=1200, poll=10)
        raw = OUT / f"{line}_raw.mp4"; kie_client.download(r["urls"][0], str(raw))
        grd = OUT / f"{line}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-vf", GRADE, "-c:v", "libx264", "-crf", "18", "-c:a", "copy", str(grd)], check=True)
        return {"line": line, "expr": expr, "cr": r.get("credits")}
    except Exception as e:
        return {"line": line, "err": str(e)[:150]}


def main(lines):
    print(f"bal before: {kie_client.credits()} | {len(lines)} Indi lines", flush=True)
    spent = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for d in ex.map(worker, lines):
            if d.get("err"):
                print(f"  FAIL {d['line']}: {d['err']}", flush=True)
            else:
                spent += d.get("cr") or 0; print(f"  OK {d['line']} ({d['expr']}) {d.get('cr')}cr", flush=True)
    print(f"bal after: {kie_client.credits()} | ~{spent}cr", flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["wave1"]:
        lines = WAVE1
    elif a == ["rest"]:
        done = {p.stem for p in OUT.glob("*.mp4") if not p.stem.endswith("_raw")}
        lines = [l for l in CU if l not in done]
    elif a == ["all"] or not a:
        lines = list(CU)
    else:
        lines = a
    main(lines)
