"""Per-PLATE calibration — authored ONCE per plate (any episode), reused by every line on it.

plate json (episodes/<ep>/lipsync/plates/<plate_id>.json):
{
  "plate_id": "ep3_strong_ts",
  "video": "scratch/ep3/bridges/strong_ts/shot_fix.mp4",   // repo-relative
  "character": "bentley",
  "angle": "three_quarter",                 // which shape sheet this framing uses
  "template_box": [565, 495, 715, 580],     // MOUTH-REGION template in frame-0 px (not the nose!)
  "mouth_offset": [75, 42],                 // mouth anchor relative to template top-left
  "mouth_width": 140,                       // patch width in plate px
  "track_fps": 12, "min_score": 0.60, "search_radius_px": 60,
  "visibility": [[0.0, 2.85]]               // windows where the mouth is readable; empty=always
}

The computed track is cached next to the calibration (<plate_id>.track.json) and reused."""
import json
import statistics
from pathlib import Path

from bentley.lipsync.mouth_autotrack import autotrack
from bentley.lipsync.mouth_track import MouthTrack

ROOT = Path(__file__).resolve().parents[2]


class Plate:
    def __init__(self, config_path):
        self.path = Path(config_path)
        cfg = json.loads(self.path.read_text())
        self.plate_id = cfg["plate_id"]
        self.video = ROOT / cfg["video"]
        self.character = cfg["character"]
        self.angle = cfg.get("angle")
        self.template_box = tuple(cfg["template_box"])
        self.mouth_offset = tuple(cfg["mouth_offset"])
        self.mouth_width = cfg["mouth_width"]
        self.track_fps = cfg.get("track_fps", 12)
        self.min_score = cfg.get("min_score", 0.60)
        self.search_radius_px = cfg.get("search_radius_px", 60)
        self.visibility = [tuple(w) for w in cfg.get("visibility", [])]
        if not self.video.exists():
            raise FileNotFoundError(f"plate video missing: {self.video}")

    def _visible(self, t):
        if not self.visibility:
            return True
        return any(a <= t <= b for a, b in self.visibility)

    def track(self, workdir=None, refresh=False):
        """The plate's mouth track — computed once (windowed NCC + median filter + visibility),
        cached as <plate_id>.track.json, reused by every line on this plate."""
        cache = self.path.parent / f"{self.plate_id}.track.json"
        if cache.exists() and not refresh:
            t = MouthTrack.load(cache)
            t.template_width_px = self.mouth_width
            return t
        t = autotrack(self.video, self.template_box, self.mouth_offset,
                      fps=self.track_fps, workdir=workdir,
                      min_score=self.min_score, search_radius_px=self.search_radius_px)
        for key in ("x", "y"):  # median filter (window 7): transient glitches -> consensus
            vals = [k[key] for k in t.kf]
            for i, k in enumerate(t.kf):
                lo, hi = max(0, i - 3), min(len(vals), i + 4)
                k[key] = statistics.median(vals[lo:hi])
        for k in t.kf:
            k["visible"] = self._visible(k["time"])
        t.save(cache)
        t.template_width_px = self.mouth_width
        return t
