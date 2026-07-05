"""Project viseme names + the Rhubarb->project mapping (plan §Rhubarb To Project Viseme Mapping).

HARD RULE (verified blocker in review): only Rhubarb `X` (rest) and `A` (M/B/P lip closure) may map
to a fully closed mouth. Rhubarb `B` is a SPEECH shape (slightly-open consonants + EE, ~half of all
voiced time) — mapping it closed produces a ventriloquist. Enforced by tests/test_lipsync_visemes.py."""

# Internal shape names (v1 minimum set — all authored TOOTHLESS, owner-locked 2026-07-01)
SHAPES = ["REST_CLOSED", "MBP", "CONS", "AI", "E", "O", "U", "FV", "L"]
# Optional v2+ helpers (angle variants, OPEN_JAW, BREATH) are additive; renderer falls back per map.
CLOSED_SHAPES = {"REST_CLOSED", "MBP"}

# Rhubarb Preston-Blair cue -> project viseme. Deterministic (no "or" — review amendment).
RHUBARB_MAP = {
    "A": "MBP",          # lip closure for M/B/P
    "B": "CONS",         # slightly-open consonants + EE — NEVER closed
    "C": "AI",           # open vowel
    "D": "AI",           # wide-open AA -> OPEN_JAW when a set has it; v1 falls back to AI (full)
    "E": "O",            # rounded mid-open
    "F": "U",            # puckered/rounded
    "G": "FV",           # F/V contact (dog-safe redesign)
    "H": "L",            # tongue-forward L
    "X": "REST_CLOSED",  # silence/rest
}


def map_cue(rhubarb_value, available=None):
    """Map one Rhubarb cue value to a project viseme, honoring the available shape set."""
    if rhubarb_value not in RHUBARB_MAP:
        raise ValueError(f"unknown Rhubarb cue {rhubarb_value!r} (expected {sorted(RHUBARB_MAP)})")
    v = RHUBARB_MAP[rhubarb_value]
    if rhubarb_value == "D" and available and "OPEN_JAW" in available:
        return "OPEN_JAW"
    if available and v not in available:
        raise ValueError(f"viseme {v!r} not in the loaded shape set {sorted(available)}")
    return v


def validate_cues(cues):
    """Validate an ordered [{start,end,viseme}] timeline: known names, sane + non-overlapping times."""
    prev_end = -1.0
    for c in cues:
        if c["viseme"] not in SHAPES and c["viseme"] != "OPEN_JAW":
            raise ValueError(f"unknown viseme {c['viseme']!r}")
        if c["end"] <= c["start"]:
            raise ValueError(f"cue has non-positive duration: {c}")
        if c["start"] < prev_end - 1e-6:
            raise ValueError(f"cue overlaps previous (prev_end={prev_end:.3f}): {c}")
        prev_end = c["end"]
    return cues
