"""Per-PLATE mouth track: where the mouth anchor sits over time (x, y, scale, rotation, visible).

Tracks are keyed by PLATE (reused across every line on that plate with time offsets), interpolated
linearly between keyframes. Deterministic by construction."""
import json
from pathlib import Path


class MouthTrack:
    def __init__(self, keyframes, fps=24, coordinate_space="source_video_pixels"):
        if not keyframes:
            raise ValueError("mouth track needs at least one keyframe")
        self.kf = sorted(keyframes, key=lambda k: k["time"])
        self.fps = fps
        self.coordinate_space = coordinate_space

    @classmethod
    def load(cls, path):
        d = json.loads(Path(path).read_text())
        return cls(d["keyframes"], d.get("video_fps", 24),
                   d.get("coordinate_space", "source_video_pixels"))

    def save(self, path):
        Path(path).write_text(json.dumps(
            {"video_fps": self.fps, "coordinate_space": self.coordinate_space,
             "keyframes": self.kf}, indent=2))

    def at(self, t):
        """Interpolated {x, y, scale, rotation_deg, visible} at time t (clamped to track range)."""
        kf = self.kf
        if t <= kf[0]["time"]:
            return dict(kf[0])
        if t >= kf[-1]["time"]:
            return dict(kf[-1])
        for a, b in zip(kf, kf[1:]):
            if a["time"] <= t <= b["time"]:
                f = (t - a["time"]) / max(1e-9, b["time"] - a["time"])
                lerp = lambda p, q: p + (q - p) * f
                out = {"time": t, "visible": a.get("visible", True) and b.get("visible", True)}
                # interpolate every shared numeric key (x, y, scale, rotation_deg, angle_ratio, ...)
                for k in a:
                    if k in ("time", "visible"):
                        continue
                    va, vb = a.get(k), b.get(k, a.get(k))
                    if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
                        out[k] = lerp(va, vb)
                out.setdefault("scale", 1.0)
                out.setdefault("rotation_deg", 0.0)
                return out
        raise AssertionError("unreachable")
