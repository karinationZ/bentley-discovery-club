#!/usr/bin/env python3
"""EP3 lip-sync batch — every Bentley/Marco dialogue line through Kling-Avatar (mouth == the line's audio),
driven from a tight front-facing face-CU keyframe (the proven method). Grades the Avatar output (it darkens).
Out: scratch/ep3/talk/<LABEL>.mp4. Run: python3 episodes/ep3/talk_batch.py"""
import sys, time, subprocess, concurrent.futures
from pathlib import Path
ROOT = Path("/project"); sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host
KEYS = ROOT / "scratch/ep3/talk_keys"; VO = ROOT / "episodes/ep3/vo"; OUT = ROOT / "scratch/ep3/talk"; OUT.mkdir(parents=True, exist_ok=True)
GRADE = "eq=brightness=0.05:saturation=1.06:contrast=1.04,unsharp=3:3:0.4:3:3:0.0,format=yuv420p"
BP = "Bentley the red-fawn Boxer puppy talks naturally, {e}, natural dog mouth, NO human teeth, NO human grin, soft warm eyes, on-model, gentle lively head motion."
MP = "Marco the boy ant talks, {e}, big boyish eyes, antennae moving, toothless, RICH GOLDEN-AMBER body (honey/copper-gold, NOT neon yellow), on-model, lively."
# label -> (keyframe, prompt)
LINES = {
 "B_hook1": ("bentley_happy", BP.format(e="playful and curious")),
 "B_findline": ("bentley_happy", BP.format(e="delighted and excited")),
 "B_tooheavy": ("bentley_happy", BP.format(e="warm and eager")),
 "B_whatline": ("bentley_neutral", BP.format(e="puzzled and curious")),
 "B_zoomit": ("bentley_happy", BP.format(e="bouncy and excited")),
 "B_oops": ("bentley_worried", BP.format(e="sheepish and guilty")),
 "B_realize": ("bentley_worried", BP.format(e="a worried realization turning to resolve")),
 "B_smellit": ("bentley_neutral", BP.format(e="curious and discovering")),
 "B_crosseyed": ("bentley_happy", BP.format(e="giggly and ticklish")),
 "B_dontgrab": ("bentley_happy", BP.format(e="brave and determined")),
 "B_strong": ("bentley_warm", BP.format(e="warm and affirming")),
 "B_youarecity": ("bentley_happy", BP.format(e="joyful and emphatic")),
 "B_lesson": ("bentley_warm", BP.format(e="warm and earnest")),
 "B_promise": ("bentley_catch", BP.format(e="calm, alert and engaged -- the catchphrase, eyes open head-tilt")),
 "B_deepdrop": ("bentley_worried", BP.format(e="curious and a little alarmed")),
 "M_igotit": ("marco_excited", MP.format(e="confident and cheeky")),
 "M_smellpath": ("marco_neutral", MP.format(e="explaining patiently")),
 "M_waitno": ("marco_worried", MP.format(e="alarmed and urgent")),
 "M_lost": ("marco_worried", MP.format(e="panicked and scared")),
 "M_youstopped": ("marco_excited", MP.format(e="hopeful and amazed")),
 "M_checkyou": ("marco_neutral", MP.format(e="curious and gentle")),
 "M_brave": ("marco_neutral", MP.format(e="warm and sincere")),
 "M_together": ("marco_excited", MP.format(e="rallying and triumphant")),
 "M_nobody": ("marco_worried", MP.format(e="small, sad and wistful")),
 "M_comesee": ("marco_excited", MP.format(e="urgent and eager")),
}


def one(item):
    label, (kf, prompt) = item
    kfp = KEYS / f"{kf}.png"; vop = VO / f"{label}.mp3"
    if not kfp.exists() or not vop.exists():
        return f"{label} MISSING ({kfp.exists()=} {vop.exists()=})"
    img = catbox_host(str(kfp)); aud = catbox_host(str(vop))
    for a in range(5):
        try:
            r = kie_client.run("kling/ai-avatar-standard", {"image_url": img, "audio_url": aud, "prompt": prompt}, timeout=1200, poll=10)
            raw = str(OUT / f"{label}_raw.mp4"); kie_client.download(r["urls"][0], raw)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-vf", GRADE, "-c:a", "copy", str(OUT / f"{label}.mp4")], check=True)
            return f"{label}: {r.get('credits')}cr"
        except Exception as e:
            time.sleep(12); err = str(e)[:60]
    return f"{label} FAIL {err}"


def main():
    todo = list(LINES.items())
    done = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for m in ex.map(one, todo):
            done += 1; print(f"  [{done}/{len(todo)}] {m}", flush=True)


if __name__ == "__main__":
    main()
