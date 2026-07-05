"""Character registry for the lip-sync system — any character (Bentley, Marco, future guests)
is onboarded as DATA, not code: assets/lipsync/<name>/character.json + angle shape sheets.

character.json:
{
  "character": "bentley",
  "sheets": {"three_quarter": "mouth_shapes/v2_tq/manifest.json",
             "side": "mouth_shapes/v2_side/manifest.json"},
  "default_sheet": "three_quarter",
  "plate_provides": ["REST_CLOSED", "MBP", "CONS", "FV"],
  "rhubarb_map_overrides": {},        // e.g. Marco insect mouth remaps
  "min_mouth_px": 24                  // waiver: mouths smaller than this get NO viseme pass
}
"""
import json
from pathlib import Path

from bentley.lipsync.mouth_sheet import MouthSheet
from bentley.lipsync.visemes import RHUBARB_MAP

ROOT = Path(__file__).resolve().parents[2]
CHAR_DIR = ROOT / "assets/lipsync"


class Character:
    def __init__(self, config_path):
        self.path = Path(config_path)
        cfg = json.loads(self.path.read_text())
        self.name = cfg["character"]
        self.default_sheet = cfg.get("default_sheet")
        self.plate_provides = frozenset(cfg.get("plate_provides", ["REST_CLOSED", "MBP"]))
        self.min_mouth_px = cfg.get("min_mouth_px", 24)
        self.rhubarb_map = dict(RHUBARB_MAP, **cfg.get("rhubarb_map_overrides", {}))
        self.sheets = {}
        for angle, rel in cfg["sheets"].items():
            self.sheets[angle] = MouthSheet(self.path.parent / rel)
        if self.default_sheet is None:
            self.default_sheet = next(iter(self.sheets))
        if self.default_sheet not in self.sheets:
            raise ValueError(f"default_sheet {self.default_sheet!r} not in sheets")

    def sheet(self, angle=None):
        return self.sheets[angle or self.default_sheet]

    @property
    def available(self):
        return self.sheet().available


def load(name):
    """Load a character by name from assets/lipsync/<name>/character.json."""
    p = CHAR_DIR / name / "character.json"
    if not p.exists():
        have = sorted(d.name for d in CHAR_DIR.iterdir() if (d / "character.json").exists()) \
            if CHAR_DIR.exists() else []
        raise FileNotFoundError(f"no character config at {p} (onboarded: {have})")
    return Character(p)
