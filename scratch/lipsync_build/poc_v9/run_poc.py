#!/usr/bin/env python3
"""EP3 rig-POC: B_strong over the STRONG plate (mouth-closed plate -> overlay mode).
Rhubarb timing (real transcript) + owner-picked toothless shape sheet + nose autotrack + minimal comp."""
import sys
from pathlib import Path
ROOT = Path("/project"); sys.path.insert(0, str(ROOT))
from bentley.lipsync.rhubarb_adapter import transcript_for, viseme_timeline
from bentley.lipsync.mouth_autotrack import autotrack
from bentley.lipsync.mouth_sheet import MouthSheet
from bentley.lipsync.render_overlay import render
from bentley.lipsync.visemes import validate_cues

POC = ROOT / "scratch/lipsync_build/poc_v9"
PLATE = POC / "plate.mp4"
LINE_OFFSET = -0.28  # B_strong started 0.28s before this window

sheet = MouthSheet(ROOT / "assets/lipsync/bentley/mouth_shapes/v1/manifest.json")
cues = viseme_timeline(ROOT / "episodes/ep3/vo/B_strong.mp3", transcript_for("B_strong"),
                       available=sheet.available, workdir=POC / "rhubarb")
clip = [{**c, "start": c["start"] + LINE_OFFSET, "end": c["end"] + LINE_OFFSET} for c in cues]
clip = validate_cues([c for c in clip if c["end"] > 0])
print(f"cues: {len(clip)} covering {clip[0]['start']:.2f}..{clip[-1]['end']:.2f}s")

track = autotrack(PLATE, template_box=(660, 440, 790, 535), mouth_offset=(-20, 115),
                  fps=6, workdir=POC / "track")
scores = track.match_scores
print(f"track: {len(track.kf)} keys, NCC scores min/med/max = "
      f"{min(scores):.2f}/{sorted(scores)[len(scores)//2]:.2f}/{max(scores):.2f}")
track.save(POC / "strong_plate_track.json")

out = render(PLATE, clip, track, sheet, POC / "EP3_BSTRONG_RIG_POC.mp4",
             audio=PLATE, mouth_width=185, workdir=POC / "render")
print("->", out)
