#!/usr/bin/env python3
"""EP3 VO — record the whole reel from the script's `label | speaker | text` block, in script order.
B_->tts_bentley (B_stoplook/B_promise->tts_catchphrase), M_->tts_marco, N_->Bill narrator.
Run: set -a;source .env;set +a; python3 episodes/ep3/make_vo_ep3.py"""
import sys, re, subprocess
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.voices.dialogue import tts_bentley, tts_marco, tts_catchphrase
from bentley.shared import eleven
from bentley.shared.audio import clean_master

VO = ROOT / "episodes/ep3/vo"
VO.mkdir(parents=True, exist_ok=True)


def tts_narrator(text, outp):
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.NARRATOR, text, raw,
                 settings={"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.08})  # Bill runs slow; nudge up
    clean_master(raw, outp)
    return outp


def parse_lines():
    cap, out = False, []
    for ln in (ROOT / "episodes/ep3/EP3_SCRIPT.md").read_text().splitlines():
        if ln.strip().startswith("label") and "speaker" in ln:
            cap = True
            continue
        if cap:
            if ln.strip() == "```":
                break
            if "|" in ln:
                p = [x.strip() for x in ln.split("|")]
                if len(p) >= 3 and re.match(r"^[BMN]_", p[0]):
                    out.append((p[0], p[1], p[2]))
    return out


def main():
    lines = parse_lines()
    print(f"{len(lines)} VO lines", flush=True)
    order = []
    for lab, spk, text in lines:
        outp = str(VO / f"{lab}.mp3")
        if lab in ("B_stoplook", "B_promise"):
            tts_catchphrase(outp)
        elif spk == "B":
            tts_bentley(text, outp)
        elif spk == "M":
            tts_marco(text, outp)
        elif spk == "N":
            tts_narrator(text, outp)
        d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", outp]).decode())
        order.append(outp)
        print(f"  {lab:14s} {spk}  {d:4.1f}s", flush=True)
    listf = VO / "_reel.txt"
    listf.write_text("\n".join(f"file '{p}'" for p in order))
    reel = VO / "EP3_VO_reel.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listf),
                    "-ar", "44100", "-ac", "1", "-b:a", "192k", str(reel)], check=True)
    rd = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(reel)]).decode())
    print(f"REEL -> {reel}  ({rd/60:.1f} min, {len(order)} lines)", flush=True)


if __name__ == "__main__":
    main()
