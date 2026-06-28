#!/usr/bin/env python3
"""EP2 v13 talking pass — Phase 1: tight front-facing FACE-CU Bentley keyframes (the proven Ep1 Avatar
framing) from the CURRENT master, across the emotional range. Hand-pick the on-model ones; each Bentley
line is then Avatar-driven from the best-matching expression. Run: set -a;source .env;set +a
  python3 talk_keys.py            # 2 candidates per expression + contact sheets
"""
import sys, subprocess, time
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/talking_v13/keys"; OUT.mkdir(parents=True, exist_ok=True)
B_MASTER = ROOT / "assets/character_design/Bentley_MASTER_pixar.png"
B_TURN = ROOT / "assets/character_design/Bentley_MODEL_SHEET_turnaround.png"
REF_EP1 = ROOT / "assets/approved/bentley/N6_kie_key_bright2.png"   # proven Ep1 framing reference

COMMON = (
    "Tight head-and-shoulders FACE close-up of Bentley the red-fawn Boxer puppy, looking straight at the camera, "
    "front-facing, BRIGHT daylight on her face (the framing of a talking-to-camera shot). Mid-speech with her mouth "
    "slightly open -- a soft natural small-dog mouth, a little tongue and tiny puppy teeth ok, but NO human grin, NO "
    "human smile, NO bulging eyes. On-model: black face mask, grey chin, NORMAL-sized round brown eyes, floppy folded-"
    "down ears, white chest blaze, teal collar, gold paw-print tag. Warm bright tide-pool background, soft cartoony-"
    "Pixar render. Keep her EXACTLY on-model, do not redraw or restyle her. No text, no watermark. "
)
EXPR = {
    "curious": "Expression: bright, curious and alert -- eyes wide and sparkling, ears perked, a slight eager head-tilt.",
    "delighted": "Expression: delighted and joyful -- eyes shining with happiness, ears up, a happy excited energy.",
    "reassuring": "Expression: warm, gentle and reassuring -- soft loving eyes, calm and tender.",
    "playful": "Expression: playful and a little cheeky -- a mischievous sparkle in the eyes, bright and fun.",
    "calm": "Expression: calm and focused -- eyes open and attentive, a gentle, present, listening look.",
    "awe": "Expression: wide-eyed wonder and surprise -- ears lifting, amazed and curious.",
}


def make(n=2):
    inp = [catbox_host(str(B_MASTER)), catbox_host(str(B_TURN)), catbox_host(str(REF_EP1))]
    print("bal before:", kie_client.credits(), flush=True)
    rows = []
    for expr, etxt in EXPR.items():
        made = []
        for i in range(n):
            out = OUT / f"key_{expr}_{i}.png"
            if out.exists() and out.stat().st_size > 100_000:
                made.append(out); continue
            for attempt in range(1, 3):
                try:
                    res = kie_client.run("gpt-image-2-image-to-image", {"prompt": COMMON + etxt, "input_urls": inp, "aspect_ratio": "16:9"}, timeout=900, poll=8)
                    kie_client.download(res["urls"][0], str(out)); made.append(out); print(f"{expr} {i}: {res.get('credits')}cr", flush=True); break
                except Exception as e:
                    print(f"{expr} {i} fail {attempt}: {str(e)[:140]}", flush=True); time.sleep(8)
        if made:
            tmp = OUT / f"_s_{expr}"; tmp.mkdir(exist_ok=True)
            for j, p in enumerate(made):
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(p), "-vf", "scale=300:300:force_original_aspect_ratio=decrease,pad=300:300:(ow-iw)/2:(oh-ih)/2:color=0x202020", str(tmp / f"s{j}.png")], check=False)
            r = OUT / f"_row_{expr}.png"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "s%d.png"), "-vf", f"tile={len(made)}x1", str(r)], check=False)
            rows.append((expr, r))
    if rows:
        ins = []
        for expr, r in rows:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(r), "-vf", "scale=600:300", str(OUT / f"_n_{expr}.png")], check=False)
            ins.append(OUT / f"_n_{expr}.png")
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        for p in ins:
            cmd += ["-i", str(p)]
        fc = "".join(f"[{i}:v]" for i in range(len(ins))) + f"vstack={len(ins)}"
        subprocess.run(cmd + ["-filter_complex", fc, str(OUT / "key_candidates.png")], check=False)
        print(f"\nSHEET -> {OUT/'key_candidates.png'}  rows: {', '.join(e for e,_ in rows)} (each row = candidate 0,1)", flush=True)
    print("bal after:", kie_client.credits(), flush=True)


if __name__ == "__main__":
    make()
