"""Load a character's authored mouth-shape sheet (manifest + transparent patch PNGs)."""
import json
from pathlib import Path

from PIL import Image

from bentley.lipsync.visemes import SHAPES

ROOT = Path(__file__).resolve().parents[2]


class MouthSheet:
    def __init__(self, manifest_path):
        self.path = Path(manifest_path)
        m = json.loads(self.path.read_text())
        self.character = m["character"]
        self.version = m["version"]
        self.anchor = (m["anchor"]["x"], m["anchor"]["y"])
        self.images = {}
        for name, spec in m["shapes"].items():
            if name not in SHAPES and name != "OPEN_JAW":
                raise ValueError(f"manifest shape {name!r} is not a known viseme")
            f = self.path.parent / spec["file"]
            if not f.exists():
                raise FileNotFoundError(f"mouth shape PNG missing: {f}")
            self.images[name] = Image.open(f).convert("RGBA")

    @property
    def available(self):
        return set(self.images)

    def patch(self, viseme, width_px):
        """The shape image scaled so its width == width_px (aspect preserved)."""
        im = self.images[viseme]
        h = max(1, round(im.height * width_px / im.width))
        return im.resize((max(1, int(width_px)), h), Image.Resampling.LANCZOS)
