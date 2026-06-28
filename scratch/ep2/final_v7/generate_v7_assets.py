#!/usr/bin/env python3
"""Generate Ep2 v7 replacement Bentley assets.

This script is intentionally resumable and writes only to scratch/ep2/final_v7.
It does not replace production sources.
"""
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

ROOT = Path("/project")
sys.path.insert(0, str(ROOT))

from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/final_v7"
KF = OUT / "keyframes"
MO = OUT / "motion"
QA = OUT / "qa"
for d in (KF, MO, QA):
    d.mkdir(parents=True, exist_ok=True)

B_MASTER = ROOT / "assets/character_design/Bentley_MASTER_pixar.png"
B_TURN = ROOT / "assets/character_design/Bentley_MODEL_SHEET_turnaround.png"
INDI = ROOT / "assets/character_design/Indi_LOCKED.png"

COMMON_STILL = (
    "16:9 premium 3D animated kids-show keyframe in the same warm tide-pool world. "
    "Bentley is the exact young red-fawn Boxer puppy from the Bentley references. "
    "Must preserve Bentley canon: black face mask, grey chin, brown eyes, floppy folded ears down, "
    "teal collar, gold paw-print Bentley tag, white chest blaze, solid red-fawn paws with no white "
    "socks or toes, short docked tail stub only. Use the turnaround only for body anatomy and the "
    "short docked tail; ignore its shell charm. Bentley's mouth is closed and natural. "
    "Do not create a long tail, curled tail, upright tail, white paws, white toes, upright ears, "
    "adult body, different breed, human smile, human teeth, text, watermark, or captions. "
)

INDI_RULE = (
    "Indi must match the octopus reference: small soft purple California two-spot octopus, teal eyes, "
    "two teal ring spots, eight tentacles, no nose, no eyebrows, tiny toothless mouth, no teeth, no human face. "
)

COMMON_MOTION = (
    "Keep Bentley's exact identity locked from the first frame and element refs: short docked tail stub, "
    "floppy folded ears, solid red-fawn paws with no white socks/toes, black mask, teal collar, gold paw tag. "
    "Bentley's mouth stays closed and natural: no human smile, no human teeth. "
    "Stable camera, warm tide-pool light, natural water ripples, no text, no captions, no watermark."
)


@dataclass(frozen=True)
class Shot:
    sid: str
    refs: tuple[str, ...]
    still_prompt: str
    motion_prompt: str


SHOTS = [
    Shot(
        "a0_02_boop",
        ("bentley",),
        COMMON_STILL
        + "Scene: Bentley creeps low and curious toward a cute speckled tide-pool rock, one front paw lifted and reaching to gently boop the rock.",
        "Bentley takes one slow step and gently touches the speckled rock with one front paw; subtle head focus and soft water ripples. "
        + COMMON_MOTION,
    ),
    Shot(
        "a1_07_chase",
        ("bentley",),
        COMMON_STILL
        + "Scene: comedy chase beat. Bentley mid-playful-pounce among speckled tide-pool rocks as a small jet of water squirts up at her surprised face.",
        "Bentley pounces playfully; a small jet of water squirts up and she flinches back, surprised but mouth closed. "
        + COMMON_MOTION,
    ),
    Shot(
        "a1_09_lunge",
        ("bentley", "indi"),
        COMMON_STILL
        + INDI_RULE
        + "Scene: Bentley lunges forward across tide-pool rocks reaching with both front paws while a single small purple octopus arm slips away beside a tiny shell.",
        "Bentley lunges forward carefully while the small purple octopus arm slips away; the shell stays still; water ripples. "
        + COMMON_MOTION
        + " Keep Indi's arm toothless and cephalopod-like.",
    ),
    Shot(
        "a2_10_corner",
        ("bentley", "indi"),
        COMMON_STILL
        + INDI_RULE
        + "Scene: Bentley corners tiny Indi near a crevice but is not mean; Indi presses back small and worried, teal ring spots visible.",
        "Bentley leans in a little, then slows; Indi presses back small and worried, teal ring spots brighten gently. "
        + COMMON_MOTION
        + " Keep both mouths closed/toothless.",
    ),
    Shot(
        "a3_20_twoshot",
        ("bentley", "indi"),
        COMMON_STILL
        + INDI_RULE
        + "Scene: calm two-shot. Bentley sits on a tide-pool rock facing Indi; Indi is small, shy, and offering one tentacle toward Bentley.",
        "Bentley sits calmly, breathing softly; Indi slowly lifts one tentacle in trust; gentle water motion. "
        + COMMON_MOTION
        + " Keep Indi tiny, toothless, with teal eyes and teal ring spots.",
    ),
    Shot(
        "a3_23_colorchange",
        ("bentley", "indi"),
        COMMON_STILL
        + INDI_RULE
        + "Scene: bonding color-change game. Tiny Indi beside Bentley turns parts of her soft purple skin red-fawn like Bentley's coat while Bentley watches amazed.",
        "Indi's purple skin softly shifts with a red-fawn patch like Bentley's coat; Bentley watches with delighted eyes, mouth closed. "
        + COMMON_MOTION
        + " No smiling mouth; use eyes and body language for delight.",
    ),
    Shot(
        "a5_30_pawhold",
        ("bentley", "indi"),
        COMMON_STILL
        + INDI_RULE
        + "Scene: heart shot macro. Indi's small purple tentacle gently rests on Bentley's solid red-fawn paw; Bentley is calm and protective.",
        "Indi's small tentacle gently rests on Bentley's red-fawn paw; both characters breathe softly; warm emotional tide-pool light. "
        + COMMON_MOTION
        + " Keep the paw solid red-fawn with no white toes.",
    ),
    Shot(
        "a2_13_realize",
        ("bentley",),
        COMMON_STILL
        + "Scene: worried medium close-up. Bentley looks toward the eel crevice, realizing she scared Indi. Soft worried eyes, mouth closed.",
        "Bentley looks from the crevice down to the water, worried and still learning; subtle head dip, mouth closed. "
        + COMMON_MOTION,
    ),
    Shot(
        "a3_14_stoplook",
        ("bentley",),
        COMMON_STILL
        + "Scene: Bentley sits very still and calm at the tide pool, listening carefully. Soft focused eyes, mouth closed.",
        "Bentley sits still, stops, looks, and listens: tiny eye movement, soft breathing, no mouth movement. "
        + COMMON_MOTION,
    ),
    Shot(
        "a3_18_why",
        ("bentley", "indi"),
        COMMON_STILL
        + INDI_RULE
        + "Scene: Bentley gently asks Indi a question, head slightly tilted, sitting at a respectful distance. Indi is small and shy nearby.",
        "Bentley tilts her head gently toward Indi, curious and kind; Indi stays small and shy; no mouth movement. "
        + COMMON_MOTION
        + " Keep Indi toothless and non-human.",
    ),
    Shot(
        "a3_21_snackpouch",
        ("bentley", "indi"),
        COMMON_STILL
        + INDI_RULE
        + "Scene: Bentley sits patiently beside the crevice with Indi peeking out. Bentley is calm, reassuring, mouth closed.",
        "Bentley settles patiently beside the crevice while Indi peeks out; gentle breathing and water motion, no mouth movement. "
        + COMMON_MOTION,
    ),
    Shot(
        "a3_24_youdidme",
        ("bentley", "indi"),
        COMMON_STILL
        + INDI_RULE
        + "Scene: delighted reaction after Indi copies Bentley's coat color. Bentley's eyes shine with delight but her mouth remains closed; Indi is tiny and proud.",
        "Bentley bounces a little with delighted eyes while Indi shows the red-fawn color patch; mouth closed, no smile. "
        + COMMON_MOTION,
    ),
    Shot(
        "a4_27_breathe",
        ("bentley", "indi"),
        COMMON_STILL
        + INDI_RULE
        + "Scene: tender rescue beat. Bentley crouches gently near wedged Indi, giving space and encouragement. Mouth closed, soft worried eyes.",
        "Bentley crouches low and calm, backing off slightly to give Indi room; Indi tries to squeeze gently; no mouth movement. "
        + COMMON_MOTION,
    ),
    Shot(
        "a5_31_button",
        ("bentley", "indi"),
        COMMON_STILL
        + INDI_RULE
        + "Scene: emotional friendship close two-shot. Bentley sits close but gentle, looking at Indi with soft eyes. Indi is safe and seen.",
        "Bentley gazes softly at Indi, then lowers her head slightly in reassurance; Indi relaxes, safe. "
        + COMMON_MOTION,
    ),
    Shot(
        "a6_35_whereGoing",
        ("bentley",),
        COMMON_STILL
        + "Scene: curious ending beat. Bentley looks inland toward the ant trail, ears floppy, eyes curious, mouth closed.",
        "Bentley turns her head toward the inland ant trail with curious eyes; subtle body shift, mouth closed. "
        + COMMON_MOTION,
    ),
]


def duration(path: Path) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
        )
        .decode()
        .strip()
    )


def build_ref_urls():
    urls = {
        "bentley_master": catbox_host(str(B_MASTER)),
        "bentley_turn": catbox_host(str(B_TURN)),
        "indi": catbox_host(str(INDI)),
    }
    return urls


def shot_ref_urls(shot: Shot, refs: dict[str, str]) -> list[str]:
    out = [refs["bentley_master"], refs["bentley_turn"]]
    if "indi" in shot.refs:
        out.append(refs["indi"])
    return out


def generate_still(shot: Shot, refs: dict[str, str]) -> str:
    out = KF / f"{shot.sid}.png"
    if out.exists() and out.stat().st_size > 100_000:
        return f"{shot.sid}: still exists"
    payload = {
        "prompt": shot.still_prompt,
        "input_urls": shot_ref_urls(shot, refs),
        "aspect_ratio": "16:9",
    }
    for attempt in range(1, 4):
        try:
            result = kie_client.run("gpt-image-2-image-to-image", payload, timeout=900, poll=8)
            kie_client.download(result["urls"][0], str(out))
            return f"{shot.sid}: still {result.get('credits')} cr"
        except Exception as exc:
            print(f"{shot.sid}: still attempt {attempt} failed: {str(exc)[:180]}", flush=True)
            time.sleep(10)
    return f"{shot.sid}: still FAILED"


def generate_motion(shot: Shot, refs: dict[str, str]) -> str:
    out = MO / f"{shot.sid}.mp4"
    if out.exists() and out.stat().st_size > 500_000:
        return f"{shot.sid}: motion exists"
    still = KF / f"{shot.sid}.png"
    if not still.exists():
        return f"{shot.sid}: motion skipped, no still"
    still_url = catbox_host(str(still))
    elements = [
        {
            "name": "bentley",
            "description": "Bentley locked red-fawn Boxer puppy with short docked tail stub, floppy folded ears, red-fawn paws, black mask, teal collar, gold paw tag",
            "element_input_urls": [refs["bentley_master"], refs["bentley_turn"]],
        }
    ]
    if "indi" in shot.refs:
        elements.append(
            {
                "name": "indi",
                "description": "Indi locked small soft purple California two-spot octopus with teal eyes, two teal ring spots, no nose, no eyebrows, tiny toothless mouth",
                "element_input_urls": [refs["indi"], refs["indi"]],
            }
        )
    payload = {
        "prompt": shot.motion_prompt,
        "image_urls": [still_url],
        "sound": False,
        "duration": "5",
        "aspect_ratio": "16:9",
        "mode": "std",
        "multi_shots": False,
        "kling_elements": elements,
    }
    for attempt in range(1, 3):
        try:
            result = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)
            kie_client.download(result["urls"][0], str(out))
            return f"{shot.sid}: motion {result.get('credits')} cr ({duration(out):.1f}s)"
        except Exception as exc:
            print(f"{shot.sid}: motion attempt {attempt} failed: {str(exc)[:220]}", flush=True)
            time.sleep(12)
    return f"{shot.sid}: motion FAILED"


def extract_qa():
    for mp4 in sorted(MO.glob("*.mp4")):
        sid = mp4.stem
        for t in ("0.5", "2.5", "4.6"):
            out = QA / f"{sid}_{t}.png"
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", str(mp4), "-frames:v", "1", str(out)],
                check=False,
            )


def main():
    print("credits before:", kie_client.credits(), flush=True)
    refs = build_ref_urls()

    print("Generating stills...", flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(generate_still, shot, refs) for shot in SHOTS]
        for fut in as_completed(futures):
            print(fut.result(), flush=True)

    print("Generating motion...", flush=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(generate_motion, shot, refs) for shot in SHOTS]
        for fut in as_completed(futures):
            print(fut.result(), flush=True)

    extract_qa()
    print("credits after:", kie_client.credits(), flush=True)


if __name__ == "__main__":
    main()
