"""Viseme timeline -> per-frame jaw-openness curve for the 3D rig driver.

The rig's jaw bone takes a single 0..1 openness per frame; this converts the validated project
viseme timeline (from rhubarb_adapter.viseme_timeline) into that curve, with an attack/release
follower so the jaw opens a touch faster than it closes (reads as speech, not a strobe).

HARD RULE inherited from visemes.py: CONS/E/L/O/U/FV are SPEECH shapes and must have open>0
(mapping them to 0 makes a ventriloquist). Only REST_CLOSED and MBP are fully closed.
"""
import json

# project viseme -> jaw openness (0=closed, 1=widest). Tuned for a toothless dog jaw.
OPEN = {
    "REST_CLOSED": 0.00,
    "MBP":         0.00,   # M/B/P lip closure
    "FV":          0.22,   # F/V light contact
    "CONS":        0.35,   # slightly-open consonants + EE  (NEVER 0)
    "U":           0.38,   # rounded/puckered
    "E":           0.45,
    "L":           0.50,   # tongue-forward
    "O":           0.60,   # rounded mid-open
    "AI":          0.92,   # open vowel
    "OPEN_JAW":    1.00,   # widest (rhubarb D)
}

# per-frame follower limits (fraction of full range/frame @24fps)
ATTACK = 0.34   # opening speed
RELEASE = 0.20  # closing speed (slower)


def openness_curve(cues, fps=24, dur=None):
    """[{start,end,viseme}] -> {'fps','dur','open':[...]} sampled per frame with attack/release."""
    if dur is None:
        dur = cues[-1]["end"] if cues else 0.0
    n = max(1, round(dur * fps))
    # target openness per frame (nearest-cue hold)
    tgt = []
    for f in range(n):
        t = (f + 0.5) / fps
        v = 0.0
        for c in cues:
            if c["start"] <= t < c["end"]:
                v = OPEN.get(c["viseme"], 0.35)
                break
        tgt.append(v)
    # attack/release follower
    out, cur = [], 0.0
    for v in tgt:
        if v > cur:
            cur = min(v, cur + ATTACK)
        else:
            cur = max(v, cur - RELEASE)
        out.append(round(cur, 3))
    return {"fps": fps, "dur": round(dur, 3), "open": out}


def write_openness(cues, path, fps=24, dur=None):
    data = openness_curve(cues, fps=fps, dur=dur)
    with open(path, "w") as fh:
        json.dump(data, fh)
    return data
