#!/usr/bin/env python3
"""Generate Episode 2 v3 keyframes, motion clips, and QA sheets.

Source of truth:
  episodes/ep2/shotlists/ep2_v3_character_driven.json

Usage:
  python3 scratch/ep2/restart_v3/generate_v3_assets.py stills --pod p01
  python3 scratch/ep2/restart_v3/generate_v3_assets.py motion --pod p01
  python3 scratch/ep2/restart_v3/generate_v3_assets.py qa

The script is resumable. Existing non-empty outputs are skipped unless --force is passed.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable

ROOT = Path("/project")
SHOTLIST = ROOT / "episodes/ep2/shotlists/ep2_v3_character_driven.json"
OUT = ROOT / "scratch/ep2/restart_v3"
KF = OUT / "keyframes"
MO = OUT / "motion"
QA = OUT / "qa"

B_MASTER = ROOT / "assets/character_design/Bentley_MASTER_pixar.png"
B_TURN = ROOT / "assets/character_design/Bentley_MODEL_SHEET_turnaround.png"
INDI = ROOT / "assets/character_design/Indi_LOCKED.png"
INDI_OPEN = ROOT / "assets/character_design/Indi_openmouth.png"
TIDEPOOL = ROOT / "assets/character_design/TidePool_plate.jpg"

COMMON_STILL = (
    "16:9 premium 3D animated kids-show keyframe in the same bright warm tide-pool world, "
    "Pixar-quality dimensional characters, soft cinematic daylight, colorful jewel anemones, "
    "clear water ripples, cohesive style with Bentley Discovery Club. "
)

BENTLEY_LOCK = (
    "Bentley must match the locked red-fawn Boxer puppy reference: black face mask, grey chin, "
    "brown eyes, floppy folded ears down, teal collar, gold paw-print Bentley tag, white chest blaze, "
    "solid red-fawn paws with no white socks or toes, short docked tail stub only. "
    "Bentley mouth closed or tiny dark puppy-mouth opening only; no visible teeth, gums, grin, "
    "lip-corner smile, human smile, upright ears, long tail, curled tail, adult body, or different breed. "
)

INDI_LOCK = (
    "Indi must match the locked small purple California two-spot octopus reference: teal eyes, two teal "
    "ring spots, eight soft sucker-lined arms, smooth noseless face, no eyebrows, tiny round toothless "
    "cephalopod mouth. No lips, teeth, gums, snout, ears, paws, fur, collar, tag, or human face. "
)

MOTION_SAFETY = (
    "Continuous non-looping performance, no repeated gesture, no freeze-frame, no visible restart. "
    "No text, no subtitles, no captions, no watermark. Bentley mouth closed or tiny dark puppy-mouth "
    "opening only; no teeth, gums, grin, lip-corner smile, or human smile. Indi mouth stays tiny, round, "
    "and toothless. Express emotion through eyes, ears, head tilt, body bounce, tail-stub wiggle, "
    "ring spots, arms, and body posture."
)


def load_dotenv() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for raw in env.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_dotenv()
sys.path.insert(0, str(ROOT))

from bentley.shared import kie_client  # noqa: E402
from bentley.shared.hosting import catbox_host  # noqa: E402


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check)


def duration(path: Path) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
        )
        .decode()
        .strip()
    )


def load_shots() -> tuple[dict, list[dict]]:
    data = json.loads(SHOTLIST.read_text())
    shots = [s for s in data["shots"] if s.get("type") != "card"]
    return data, shots


def selected_shots(shots: list[dict], *, pod: str | None, only: set[str] | None, limit: int | None) -> list[dict]:
    out = []
    for shot in shots:
        if pod and shot.get("pod") != pod:
            continue
        if only and shot["id"] not in only:
            continue
        out.append(shot)
    return out[:limit] if limit else out


def build_ref_urls() -> dict[str, str]:
    cache_path = OUT / "_ref_urls.json"
    if cache_path.exists():
        cached = json.loads(cache_path.read_text())
        if all(cached.get(k) for k in ("bentley_master", "bentley_turn", "indi", "indi_open", "tidepool")):
            return cached
    refs = {
        "bentley_master": catbox_host(str(B_MASTER)),
        "bentley_turn": catbox_host(str(B_TURN)),
        "indi": catbox_host(str(INDI)),
        "indi_open": catbox_host(str(INDI_OPEN)),
        "tidepool": catbox_host(str(TIDEPOOL)),
    }
    cache_path.write_text(json.dumps(refs, indent=2))
    return refs


def ref_urls_for_still(shot: dict, refs: dict[str, str]) -> list[str]:
    urls = [refs["tidepool"]]
    if "bentley" in shot.get("refs", []):
        urls.extend([refs["bentley_master"], refs["bentley_turn"]])
    if "indi" in shot.get("refs", []):
        urls.extend([refs["indi"], refs["indi_open"]])
    return urls


def safety_for_shot(shot: dict, global_safety: str) -> str:
    refs = set(shot.get("refs", []))
    if "bentley" in refs and "indi" in refs:
        return global_safety
    if "bentley" in refs:
        return (
            "Continuous non-looping performance, no repeated gesture, no freeze-frame, no visible restart. "
            "Bentley mouth closed or tiny dark puppy-mouth opening only; no visible teeth, gums, grin, "
            "lip-corner smile, or human smile. Express emotion through eyes, ears, head tilt, body bounce, "
            "and tail-stub wiggle. No visible octopus, no orange creature, no extra animal unless the shot explicitly asks for it."
        )
    if "indi" in refs:
        return (
            "Continuous non-looping performance, no repeated gesture, no freeze-frame, no visible restart. "
            "Indi has a tiny round toothless cephalopod mouth, no lips, teeth, gums, nose, brows, snout, "
            "ears, paws, fur, collar, or tag. Express emotion through eyes, ring spots, arms, and body posture."
        )
    return "No text, no subtitles, no captions, no watermark."


def still_intent(shot: dict) -> str:
    text = shot["prompt_intent"]
    text = re.sub(r"\b\d+(?:\.\d+)?-\d+(?:\.\d+)?s\s*", "", text)
    text = re.sub(r"\b\d+(?:\.\d+)?s\s*", "", text)
    return text


def still_prompt(shot: dict, global_safety: str) -> str:
    bits = [COMMON_STILL]
    if "bentley" in shot.get("refs", []):
        bits.append(BENTLEY_LOCK)
    if "indi" in shot.get("refs", []):
        bits.append(INDI_LOCK)
    bits.append(
        f"Shot {shot['id']}: create ONE single cinematic keyframe, not a storyboard, not multiple panels, "
        f"not a triptych, not a contact sheet. Show the clearest central pose for this beat: {still_intent(shot)} "
    )
    bits.append(safety_for_shot(shot, global_safety))
    bits.append("Keep composition readable for a 16:9 children's episode. No text, no watermark.")
    return " ".join(bits)


def motion_prompt(shot: dict, global_safety: str) -> str:
    safety = safety_for_shot(shot, global_safety)
    return (
        f"Animate this approved keyframe for Episode 2 shot {shot['id']}. "
        f"Action: {shot['prompt_intent']} "
        f"{safety} {MOTION_SAFETY} "
        "Keep camera stable with a gentle motivated drift only. Maintain the exact first-frame character identities."
    )


def kling_elements(shot: dict, refs: dict[str, str]) -> list[dict]:
    elements: list[dict] = []
    if "bentley" in shot.get("refs", []):
        elements.append(
            {
                "name": "bentley",
                "description": (
                    "locked red-fawn Boxer puppy, black mask, grey chin, floppy folded ears down, teal collar, "
                    "gold paw tag, white chest blaze, solid red-fawn paws, short docked tail stub, natural dog "
                    "muzzle, mouth closed or tiny dark opening only, no visible teeth, no gums, no grin, no human smile"
                ),
                "element_input_urls": [refs["bentley_master"], refs["bentley_turn"]],
            }
        )
    if "indi" in shot.get("refs", []):
        elements.append(
            {
                "name": "indi",
                "description": (
                    "locked small purple California two-spot octopus, teal eyes, two teal ring spots, eight soft "
                    "sucker-lined arms, smooth noseless face, no eyebrows, tiny round toothless cephalopod mouth, "
                    "no lips, no teeth, no gums, no snout, no human smile"
                ),
                "element_input_urls": [refs["indi"], refs["indi_open"]],
            }
        )
    return elements


def generate_still(shot: dict, refs: dict[str, str], global_safety: str, *, force: bool) -> str:
    out = KF / f"{shot['id']}.png"
    if not force and out.exists() and out.stat().st_size > 100_000:
        return f"{shot['id']}: still exists"
    payload = {
        "prompt": still_prompt(shot, global_safety),
        "input_urls": ref_urls_for_still(shot, refs),
        "aspect_ratio": "16:9",
    }
    for attempt in range(1, 4):
        try:
            result = kie_client.run("gpt-image-2-image-to-image", payload, timeout=900, poll=8)
            kie_client.download(result["urls"][0], str(out))
            return f"{shot['id']}: still {result.get('credits')}cr {result.get('secs')}s"
        except Exception as exc:
            print(f"{shot['id']}: still attempt {attempt} failed: {str(exc)[:220]}", flush=True)
            time.sleep(10)
    return f"{shot['id']}: still FAILED"


def generate_motion(shot: dict, refs: dict[str, str], global_safety: str, *, force: bool) -> str:
    out = MO / f"{shot['id']}.mp4"
    if not force and out.exists() and out.stat().st_size > 500_000:
        return f"{shot['id']}: motion exists"
    still = KF / f"{shot['id']}.png"
    if not still.exists():
        return f"{shot['id']}: motion skipped, no still"
    still_url = catbox_host(str(still))
    payload = {
        "prompt": motion_prompt(shot, global_safety),
        "image_urls": [still_url],
        "sound": False,
        "duration": str(shot.get("render_duration", "5")),
        "aspect_ratio": "16:9",
        "mode": "std",
        "multi_shots": False,
        "kling_elements": kling_elements(shot, refs),
    }
    for attempt in range(1, 3):
        try:
            result = kie_client.run("kling-3.0/video", payload, timeout=1500, poll=10)
            kie_client.download(result["urls"][0], str(out))
            return f"{shot['id']}: motion {result.get('credits')}cr {duration(out):.1f}s"
        except Exception as exc:
            print(f"{shot['id']}: motion attempt {attempt} failed: {str(exc)[:260]}", flush=True)
            time.sleep(12)
    return f"{shot['id']}: motion FAILED"


def extract_qa(shots: Iterable[dict]) -> None:
    QA.mkdir(parents=True, exist_ok=True)
    for shot in shots:
        mp4 = MO / f"{shot['id']}.mp4"
        png = KF / f"{shot['id']}.png"
        if png.exists():
            run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-vf", "scale=320:-1", str(QA / f"{shot['id']}_key.png")], check=False)
        if not mp4.exists():
            continue
        dur = duration(mp4)
        times = [0.4, max(0.5, dur / 2), max(0.5, dur - 0.35)]
        for idx, t in enumerate(times):
            out = QA / f"{shot['id']}_{idx}.png"
            run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1", str(out)], check=False)


def make_contact_sheet() -> None:
    frames = sorted(QA.glob("*.png"))
    if not frames:
        return
    list_file = QA / "_sheet_inputs.txt"
    list_file.write_text("\n".join(str(p) for p in frames))
    sheet = QA / "EP2_v3_asset_QA_sheet.jpg"
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-pattern_type",
            "glob",
            "-i",
            str(QA / "*.png"),
            "-vf",
            "scale=240:-1,tile=5x20",
            "-frames:v",
            "1",
            str(sheet),
        ],
        check=False,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["stills", "motion", "qa", "all", "credits"])
    ap.add_argument("--pod")
    ap.add_argument("--only", nargs="*", help="Specific shot ids.")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()

    for d in (OUT, KF, MO, QA):
        d.mkdir(parents=True, exist_ok=True)

    data, all_shots = load_shots()
    shots = selected_shots(all_shots, pod=args.pod, only=set(args.only or []) or None, limit=args.limit)

    if args.phase == "credits":
        print(json.dumps(kie_client.credits(), indent=2))
        return

    refs = build_ref_urls()
    global_safety = data["_meta"]["prompt_safety"]

    if args.phase in ("stills", "all"):
        print("credits before:", kie_client.credits(), flush=True)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futs = [pool.submit(generate_still, shot, refs, global_safety, force=args.force) for shot in shots]
            for fut in as_completed(futs):
                print(fut.result(), flush=True)
        print("credits after stills:", kie_client.credits(), flush=True)

    if args.phase in ("motion", "all"):
        print("credits before motion:", kie_client.credits(), flush=True)
        with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 2))) as pool:
            futs = [pool.submit(generate_motion, shot, refs, global_safety, force=args.force) for shot in shots]
            for fut in as_completed(futs):
                print(fut.result(), flush=True)
        print("credits after motion:", kie_client.credits(), flush=True)

    if args.phase in ("qa", "all"):
        extract_qa(shots)
        make_contact_sheet()
        print(f"QA -> {QA}", flush=True)


if __name__ == "__main__":
    main()
