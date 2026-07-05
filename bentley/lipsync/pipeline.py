"""The one-command lip-sync pipeline — reusable for ANY character, plate, line, episode.

    python -m bentley.lipsync.pipeline \
        --plate episodes/ep3/lipsync/plates/ep3_strong_ts.json \
        --audio episodes/ep3/vo/B_strong.mp3 --label B_strong \
        --offset -0.28 --out out/B_strong_synced.mp4

Flow: character config (registry) + plate calibration (authored once per plate, track cached)
+ line audio/transcript -> Rhubarb visemes -> tracked patch render -> QA sweep contact sheet.
The QA sweep is NOT optional — inspect it frame-by-frame before using the output (hard rule)."""
import argparse
import sys
from pathlib import Path

from bentley.lipsync import characters
from bentley.lipsync.plates import Plate
from bentley.lipsync.qa_sweep import sweep
from bentley.lipsync.render_overlay import render
from bentley.lipsync.rhubarb_adapter import run_rhubarb, transcript_for
from bentley.lipsync.visemes import map_cue, validate_cues

ROOT = Path(__file__).resolve().parents[2]


def sync_line(plate_json, audio, transcript, line_offset=0.0, out_mp4=None, workdir=None,
              qa_crop=None):
    """Sync one line onto its plate. Returns (out_mp4, qa_sheet_png).

    line_offset: line start time relative to the plate clip start (negative = line already
    running when the clip starts)."""
    plate = Plate(plate_json)
    char = characters.load(plate.character)
    sheet = char.sheet(plate.angle)
    raw = run_rhubarb(audio, transcript, workdir)
    cues = [{"start": c["start"] + line_offset, "end": c["end"] + line_offset,
             "viseme": map_cue(c["value"], sheet.available), "source": f"rhubarb:{c['value']}"}
            for c in raw]
    cues = validate_cues([c for c in cues if c["end"] > 0])
    track = plate.track(workdir=workdir)
    out_mp4 = Path(out_mp4 or (Path(audio).stem + "_synced.mp4"))
    render(plate.video, cues, track, sheet, out_mp4, audio=plate.video,
           mouth_width=plate.mouth_width, workdir=workdir,
           plate_provides=char.plate_provides)
    qa_png = out_mp4.with_suffix(".qa.png")
    if qa_crop is None:
        x0, y0 = plate.template_box[0], plate.template_box[1]
        qa_crop = (max(0, x0 - 220), max(0, y0 - 180), x0 + 380, y0 + 220)
    sweep(out_mp4, qa_png, step=0.15, crop=qa_crop)
    return out_mp4, qa_png


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rig lip-sync one line onto its plate")
    ap.add_argument("--plate", required=True, help="plate calibration json")
    ap.add_argument("--audio", required=True, help="line VO (mp3/wav)")
    ap.add_argument("--label", help="line label -> transcript from the episode script")
    ap.add_argument("--transcript", help="explicit transcript text (overrides --label)")
    ap.add_argument("--script-md", help="episode script md for --label lookup")
    ap.add_argument("--offset", type=float, default=0.0, help="line start rel. to clip start")
    ap.add_argument("--out", help="output mp4")
    a = ap.parse_args(argv)
    if a.transcript:
        tx = a.transcript
    elif a.label:
        tx = transcript_for(a.label, **({"script_md": a.script_md} if a.script_md else {}))
    else:
        ap.error("need --transcript or --label")
    out, qa = sync_line(a.plate, a.audio, tx, a.offset, a.out)
    print(f"synced -> {out}\nQA SHEET (inspect EVERY frame before shipping) -> {qa}")


if __name__ == "__main__":
    sys.exit(main())
