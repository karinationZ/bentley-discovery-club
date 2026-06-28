#!/usr/bin/env python3
"""EP2 v13 — fresh 'speaker-talks, listener-still' TWO-SHOTS for 12 conversational beats (6 Bentley-talks,
6 Indi-talks). Keyframe = both on-model, the SPEAKER mouth-open, the LISTENER mouth-closed; Kling 3.0 i2v
animates only the speaker's mouth. Run: set -a;source .env;set +a
  python3 twoshots.py keys            # 1 keyframe per beat (content-filter retries)
  python3 twoshots.py motion <id>...  # Kling the picked keyframes (or 'all')
"""
import sys, subprocess, time, concurrent.futures
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/twoshots"; OUT.mkdir(parents=True, exist_ok=True)
B_MASTER = ROOT / "assets/character_design/Bentley_MASTER_pixar.png"
B_TURN = ROOT / "assets/character_design/Bentley_MODEL_SHEET_turnaround.png"
INDI = ROOT / "assets/character_design/Indi_LOCKED.png"
INDI_SHEET = ROOT / "assets/character_design/Indi_MODEL_SHEET.png"

# line -> (speaker B/I, scene)
BEATS = {
    "P1_B03": ("B", "bright cold-open tide pool, Bentley meeting the little rock-octopus"),
    "P2_B01": ("B", "bright tide pool, Bentley watching her friend closely"),
    "P3_B01": ("B", "tide pool near a rocky crevice, Bentley curious"),
    "P4_B03": ("B", "tide pool, Bentley's gold paw-print collar tag catching the light, Bentley's full head AND upper body clearly in frame (not a cropped floating head), all four paws or chest visible on the rock"),
    "P5_B05": ("B", "beside the rocky crevice, Bentley encouraging her friend"),
    "P6_B01": ("B", "cozy warm tide pool at golden hour, a fond recap moment"),
    "P1_I04": ("I", "bright cold-open tide pool, Indi half-out of the rock"),
    "P2_I04": ("I", "bright tide pool, Indi looking smug and clever"),
    "P3_I01": ("I", "tide pool by the crevice, Indi explaining cheerfully"),
    "P5_I06": ("I", "beside the rocky crevice, Indi wry and dry"),
    "P6_I05": ("I", "tide pool, Indi turning to point inland"),
    "P6_I01": ("I", "cozy warm tide pool, Indi proud, showing off"),
}
BENT = ("BENTLEY the red-fawn Boxer puppy: black face mask, grey chin, floppy folded-down ears, white chest blaze, teal "
        "collar, gold paw-print tag, solid red-fawn paws no socks, short docked tail stub, no human grin")
IND = ("INDI the small purple octopus: teal eyes, two teal ring eyespots, eight soft arms, no nose, no eyebrows, toothless, no human face")


def key_prompt(spk, scene):
    talk, listen = (BENT, IND) if spk == "B" else (IND, BENT)
    tname = "Bentley" if spk == "B" else "Indi"
    lname = "Indi" if spk == "B" else "Bentley"
    return (f"16:9 premium 3D animated kids-show TWO-SHOT, {scene}, cartoony-Pixar style. Both characters clearly on screen "
            f"together in ONE frame, interacting. {tname} is mid-chat, her mouth softly open as she happily talks (small "
            f"natural mouth, no human grin); {lname} LISTENS, mouth CLOSED, attentive and calm. {talk}. {listen}. Warm cove "
            "light. On-model, do not restyle. No text, no watermark.")


def motion_prompt(spk):
    if spk == "B":
        return ("Bentley talks to Indi -- her mouth opens and closes as she happily speaks, ears bouncing, bright engaged "
                "eyes, a small lean-in. Indi LISTENS, mostly still, mouth CLOSED, gentle blinks and one soft arm shift. Only "
                "Bentley's mouth moves. Both on screen, warm conversation. Keep both on-model (Bentley docked tail/floppy "
                "ears/no human grin; Indi purple/teal eyes/toothless). Continuous non-looping, no freeze. No text.")
    return ("Indi talks to Bentley -- her small toothless mouth opens and closes as she speaks, teal eyes bright, a soft arm "
            "gesture. Bentley LISTENS, mostly still, mouth CLOSED, ears perked, gentle blink and head tilt. Only Indi's mouth "
            "moves. Both on screen, warm conversation. Keep both on-model (Indi purple/teal eyes/two ring spots/toothless; "
            "Bentley docked tail/floppy ears/no human grin). Continuous non-looping, no freeze. No text.")


def make_keys():
    inp = [catbox_host(str(B_MASTER)), catbox_host(str(B_TURN)), catbox_host(str(INDI)), catbox_host(str(INDI_SHEET))]
    print("bal before:", kie_client.credits(), flush=True)
    for line, (spk, scene) in BEATS.items():
        d = OUT / line; d.mkdir(exist_ok=True); key = d / "key.png"
        if key.exists():
            continue
        for attempt in range(1, 5):
            try:
                res = kie_client.run("gpt-image-2-image-to-image", {"prompt": key_prompt(spk, scene), "input_urls": inp, "aspect_ratio": "16:9"}, timeout=900, poll=8)
                kie_client.download(res["urls"][0], str(key)); print(f"{line} ({spk}): {res.get('credits')}cr", flush=True); break
            except Exception as e:
                print(f"{line} attempt {attempt}: {str(e)[:90]}", flush=True); time.sleep(6)
    # contact sheet
    rows = []
    for line in BEATS:
        k = OUT / line / "key.png"
        if k.exists():
            t = OUT / f"_s_{line}.png"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(k), "-vf", "scale=300:169,drawtext=text='" + line + "':x=6:y=6:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.5" if False else "scale=300:169", str(t)], check=False)
            rows.append(t)
    if rows:
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        for p in rows:
            cmd += ["-i", str(p)]
        n = len(rows); fc = "".join(f"[{i}:v]" for i in range(n)) + f"tile=3x{(n + 2) // 3}"
        subprocess.run(cmd + ["-filter_complex", fc, str(OUT / "keys_sheet.png")], check=False)
        print(f"-> {OUT/'keys_sheet.png'}  order: {list(BEATS)}", flush=True)
    print("bal after:", kie_client.credits(), flush=True)


def one_motion(line):
    spk = BEATS[line][0]; key = OUT / line / "key.png"
    if not key.exists():
        return {"line": line, "err": "no key"}
    elements = [
        {"name": "bentley", "description": "Bentley locked red-fawn Boxer puppy, black mask, floppy ears, red-fawn paws no socks, teal collar, gold tag, docked tail stub, no human grin", "element_input_urls": [catbox_host(str(B_MASTER)), catbox_host(str(B_TURN))]},
        {"name": "indi", "description": "Indi locked small purple two-spot octopus, teal eyes, two ring spots, no nose, no eyebrows, toothless", "element_input_urls": [catbox_host(str(INDI)), catbox_host(str(INDI_SHEET))]},
    ]
    payload = {"prompt": motion_prompt(spk), "image_urls": [catbox_host(str(key))], "sound": False, "duration": "5", "aspect_ratio": "16:9", "mode": "std", "multi_shots": False, "kling_elements": elements}
    for i in range(2):
        try:
            r = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)
            kie_client.download(r["urls"][0], str(OUT / line / "shot.mp4")); return {"line": line, "cr": r.get("credits")}
        except Exception as e:
            time.sleep(10); err = str(e)[:120]
    return {"line": line, "err": err}


def make_motion(lines):
    print("bal before:", kie_client.credits(), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for d in ex.map(one_motion, lines):
            print(f"  {'OK' if not d.get('err') else 'FAIL'} {d['line']} {d.get('cr') or d.get('err')}", flush=True)
    print("bal after:", kie_client.credits(), flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "keys":
        make_keys()
    elif a and a[0] == "motion":
        make_motion(list(BEATS) if a[1:] == ["all"] else a[1:])
