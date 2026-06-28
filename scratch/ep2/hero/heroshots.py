#!/usr/bin/env python3
"""EP2 hero shots H2-H8 (the approved fresh-Kling list, minus H1 camo which has its own script).
KIE: gpt-image-2 stills (4 candidates each, human-picked) -> kling-3.0/video motion. Never auto-batch.
Run: set -a;source .env;set +a
  python3 scratch/ep2/hero/heroshots.py stills            # all 7 shots' candidates + contact sheets
  python3 scratch/ep2/hero/heroshots.py motion <shotid> --pick N
"""
import argparse, subprocess, sys, time
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/hero"
B_MASTER = ROOT / "assets/character_design/Bentley_MASTER_pixar.png"
B_TURN = ROOT / "assets/character_design/Bentley_MODEL_SHEET_turnaround.png"
INDI = ROOT / "assets/character_design/Indi_LOCKED.png"
INDI_SHEET = ROOT / "assets/character_design/Indi_MODEL_SHEET.png"

STYLE = "16:9 premium 3D animated kids-show keyframe, warm tide-pool world, cartoony-Pixar style. "
BENTLEY_RULE = (
    "BENTLEY is the exact young red-fawn Boxer puppy: black face mask, grey chin, brown eyes, floppy folded-down ears, "
    "white chest blaze, solid red-fawn paws with NO white socks/toes, short docked tail stub only, teal collar, gold "
    "paw-print tag, mouth closed and natural (no human smile, no human teeth). "
)
INDI_RULE = (
    "INDI is the small soft purple California two-spot octopus: teal eyes, two teal ring eyespots, eight soft arms, no "
    "nose, no eyebrows, tiny closed toothless mouth, no teeth, no tooth-like sucker rows facing camera, no human face. "
)
MOTION_BASE = "Continuous non-looping performance, no repeated gesture, no freeze. Warm tide-pool light. No text, no watermark. "
MOTION_B = "Keep Bentley's identity locked: docked tail stub, floppy ears, red-fawn paws no socks, teal collar, gold tag, mouth closed, no human teeth or smile. "
MOTION_I = "Keep Indi on-model: teal eyes, two teal ring eyespots, toothless, no tooth-like suckers facing camera. "

SHOTS = {
    "H2_extremely_bentley": dict(refs=("b", "i"),
        scene="Tiny Indi beside Bentley turns her whole body the exact RED-FAWN colour of Bentley's coat; Bentley watches, delighted, eyes shining, mouth closed.",
        motion="Indi's purple skin blooms fully red-fawn to match Bentley's coat; Bentley reacts with delighted eyes and a little body bounce, mouth closed."),
    "H3_brave_outfit": dict(refs=("b", "i"),
        indi_rule="INDI here has copied Bentley and turned the SAME warm RED-FAWN colour as Bentley's coat (NOT purple): two teal ring eyespots still visible, eight soft arms, no nose, no eyebrows, tiny closed toothless mouth, no tooth-like suckers facing camera, no human face. ",
        scene="Joyful close two-shot: the tiny RED-FAWN octopus strikes a proud brave little pose; Bentley beams with pure happy-dog joy -- soft shining eyes, ears up, TONGUE OUT and relaxed, mouth soft, absolutely NO teeth and NO human smile.",
        motion="The little red-fawn octopus gives a brave proud wiggle; Bentley bounces with happy-dog joy, ears up, tongue lolling out, eyes shining, mouth soft, no teeth, no human smile."),
    "H4_stop": dict(refs=("b",),
        scene="Bentley sits very still and calm at the tide pool, eyes softly closed, the gold paw-print Listening Tag on her collar glowing warm; peaceful, happy not sad.",
        motion="Bentley sits, goes still, eyes softly close; the gold Listening Tag glows brighter; gentle breathing, tiny ear movement, no mouth movement."),
    "H5_escape": dict(refs=("i",),
        scene="ONLY the octopus -- NO dog anywhere in frame. Close on Indi mid-escape: her soft boneless purple body is SQUEEZING THROUGH a narrow slot between two rocks no wider than a coin -- the front half already through and reformed on the far side while the rest of her compresses thin to follow, like soft dough pushed through a ring. Teal eyes, two teal ring eyespots, toothless. Reads clearly that she fits her whole body through an impossibly small gap.",
        motion="Indi POURS her whole soft body through the coin-narrow rock slot like water -- compressing thin, flowing through, then reforming whole and proud on the far side. NO dog in frame. Smooth boneless squeeze, the hero science moment."),
    "H6_champion": dict(refs=("b", "i"),
        scene="Bentley lowers to eye level with tiny worried Indi wedged near a crevice, calm and encouraging, mouth closed; Indi's ring spots dimming as she calms.",
        motion="Bentley lowers her head calmly to Indi's level, reassuring; Indi's eyespots soften from bright to calm; gentle, no mouth movement on Bentley."),
    "H7_watch": dict(refs=("b", "i"),
        scene="Indi gestures like a tiny show-off beside Bentley on a tide-pool rock; Bentley leans in, whole-body curious and excited, mouth closed.",
        motion="Indi lifts an arm like a tiny magician about to perform; Bentley leans in, ears perked, eyes wide and curious, mouth closed."),
    "H8_friendship": dict(refs=("b", "i"),
        scene="Warm emotional close two-shot: Bentley and tiny Indi nestled together by the tide pool in soft golden light, safe and content; Bentley's eyes soft, mouth closed.",
        motion="Bentley and Indi settle close together, both relaxed and content; Bentley's eyes soft, gentle breathing; Indi's arms curl gently; warm golden light."),
}


def refs_for(spec):
    urls = {"b": [catbox_host(str(B_MASTER)), catbox_host(str(B_TURN))], "i": [catbox_host(str(INDI)), catbox_host(str(INDI_SHEET))]}
    out = []
    if "b" in spec["refs"]:
        out += urls["b"]
    if "i" in spec["refs"]:
        out += urls["i"]
    return out, urls


def make_stills(n=4):
    print("credits before:", kie_client.credits(), flush=True)
    for sid, spec in SHOTS.items():
        d = OUT / sid; d.mkdir(parents=True, exist_ok=True)
        inputs, _ = refs_for(spec)
        prompt = STYLE + (BENTLEY_RULE if "b" in spec["refs"] else "") + (spec.get("indi_rule", INDI_RULE) if "i" in spec["refs"] else "") + "Scene: " + spec["scene"] + " No text, no watermark."
        made = []
        for i in range(n):
            out = d / f"still_{i}.png"
            if out.exists() and out.stat().st_size > 100_000:
                made.append(out); continue
            for attempt in range(1, 3):
                try:
                    res = kie_client.run("gpt-image-2-image-to-image", {"prompt": prompt, "input_urls": inputs, "aspect_ratio": "16:9"}, timeout=900, poll=8)
                    kie_client.download(res["urls"][0], str(out)); made.append(out)
                    print(f"{sid} still {i}: {res.get('credits')} cr", flush=True); break
                except Exception as e:
                    print(f"{sid} still {i} fail {attempt}: {str(e)[:160]}", flush=True); time.sleep(8)
        if made:
            tmp = d / "_s"; tmp.mkdir(exist_ok=True)
            for j, p in enumerate(made):
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(p), "-vf", "scale=440:248:force_original_aspect_ratio=decrease,pad=440:248:(ow-iw)/2:(oh-ih)/2:color=0x202020", str(tmp / f"s{j}.png")], check=False)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "s%d.png"), "-vf", f"tile={len(made)}x1", str(d / "candidates.png")], check=False)
            print(f"  -> {d/'candidates.png'}", flush=True)
    print("credits after:", kie_client.credits(), flush=True)


def make_motion(sid, pick):
    spec = SHOTS[sid]; d = OUT / sid; still = d / f"still_{pick}.png"
    if not still.exists():
        sys.exit(f"no {still}")
    elements = [{"name": "bentley", "description": "Bentley locked red-fawn Boxer puppy, docked tail stub, floppy folded ears, red-fawn paws no socks, black mask, teal collar, gold paw tag, mouth closed no teeth", "element_input_urls": [catbox_host(str(B_MASTER)), catbox_host(str(B_TURN))]}] if "b" in spec["refs"] else []
    if "i" in spec["refs"]:
        elements.append({"name": "indi", "description": "Indi locked small purple two-spot octopus, teal eyes, two teal ring eyespots, no nose, no eyebrows, tiny toothless mouth, no tooth-like suckers", "element_input_urls": [catbox_host(str(INDI)), catbox_host(str(INDI_SHEET))]})
    safe = MOTION_BASE + (MOTION_B if "b" in spec["refs"] else "") + (MOTION_I if "i" in spec["refs"] else "")
    payload = {"prompt": spec["motion"] + " " + safe, "image_urls": [catbox_host(str(still))], "sound": False, "duration": "5", "aspect_ratio": "16:9", "mode": "std", "multi_shots": False, "kling_elements": elements}
    print("credits before:", kie_client.credits(), flush=True)
    for attempt in range(1, 3):
        try:
            res = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)
            kie_client.download(res["urls"][0], str(d / f"{sid}.mp4")); print(f"{sid} motion: {res.get('credits')} cr -> {d/(sid+'.mp4')}", flush=True)
            for t in ("0.5", "2.5", "4.5"):
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", str(d / f"{sid}.mp4"), "-frames:v", "1", str(d / f"qa_{t}.png")], check=False)
            break
        except Exception as e:
            print(f"{sid} motion fail {attempt}: {str(e)[:200]}", flush=True); time.sleep(10)
    print("credits after:", kie_client.credits(), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("stage", choices=["stills", "motion"]); ap.add_argument("shot", nargs="?"); ap.add_argument("--pick", type=int)
    a = ap.parse_args()
    if a.stage == "stills":
        make_stills()
    else:
        make_motion(a.shot, a.pick)
