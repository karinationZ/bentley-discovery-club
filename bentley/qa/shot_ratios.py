#!/usr/bin/env python3
"""Shot-Flow ratio check (SKILL §5a / playbook Part 4) — measured, not eyeballed.
Reads a shotlist JSON and sums per-piece durations by `scale` tag:
  solo_cu   -> solo talking-head runtime  (target <= ~35%)
  two_shot  -> two-shot/interaction runtime (target >= ~25%)
  wide / medium / insert / card / title -> neutral
Pieces may be flat shots ({id,dur,scale,...}) or section entries ({id,seq:[{src,dur,scale}]}).
Untagged pieces FAIL the check — the ratios are only free arithmetic if the EDL carries the tags.
Run: python -m bentley.qa.shot_ratios episodes/<ep>/shotlists/<list>.json
Exit 0 = tags complete and ratios in range; exit 1 otherwise (usable as an Animatic-Lock gate)."""
import json
import sys
from pathlib import Path

SOLO = {"solo_cu", "solo", "cu"}
TWO = {"two_shot", "two-shot", "twoshot", "interaction"}
NEUTRAL = {"wide", "medium", "insert", "card", "title", "establishing"}
SOLO_MAX = 35.0
TWO_MIN = 25.0


def pieces(shot):
    """Yield (label, dur, scale) for every piece of a shot (flat or seq-based)."""
    seq = shot.get("seq")
    if seq:
        for i, p in enumerate(seq):
            yield (f"{shot.get('id', '?')}[{i}]", float(p.get("dur", 0) or 0),
                   (p.get("scale") or shot.get("scale") or "").lower())
    else:
        yield (shot.get("id", "?"), float(shot.get("dur", 0) or 0),
               (shot.get("scale") or "").lower())


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print(__doc__)
        return 2
    data = json.loads(Path(argv[0]).read_text())
    shots = data["shots"] if isinstance(data, dict) else data

    totals = {}
    untagged = []
    total_dur = 0.0
    for shot in shots:
        for label, dur, scale in pieces(shot):
            total_dur += dur
            if not scale:
                untagged.append(label)
            else:
                totals[scale] = totals.get(scale, 0.0) + dur

    if not total_dur:
        print("shot_ratios: no durations found — is this a shotlist JSON?")
        return 1

    solo = sum(d for s, d in totals.items() if s in SOLO)
    two = sum(d for s, d in totals.items() if s in TWO)
    unknown = sorted(s for s in totals if s not in SOLO | TWO | NEUTRAL)

    print(f"total runtime (EDL): {total_dur:.1f}s")
    for s in sorted(totals, key=totals.get, reverse=True):
        print(f"  {s:12} {totals[s]:6.1f}s  {100 * totals[s] / total_dur:5.1f}%")
    solo_pct, two_pct = 100 * solo / total_dur, 100 * two / total_dur
    print(f"solo heads: {solo_pct:.1f}% (max ~{SOLO_MAX:.0f}%)   "
          f"two-shots: {two_pct:.1f}% (min ~{TWO_MIN:.0f}%)")

    ok = True
    if untagged:
        print(f"FAIL: {len(untagged)} piece(s) missing a `scale` tag: {', '.join(untagged[:12])}"
              + (" …" if len(untagged) > 12 else ""))
        ok = False
    if unknown:
        print(f"FAIL: unknown scale tag(s): {', '.join(unknown)} "
              f"(use: solo_cu / two_shot / wide / medium / insert / card / title)")
        ok = False
    if solo_pct > SOLO_MAX:
        print(f"FAIL: solo-head runtime {solo_pct:.1f}% exceeds ~{SOLO_MAX:.0f}% (Shot-Flow Law)")
        ok = False
    if two_pct < TWO_MIN:
        print(f"FAIL: two-shot runtime {two_pct:.1f}% below ~{TWO_MIN:.0f}% (Shot-Flow Law)")
        ok = False
    print("PASS" if ok else "NOT PASSED — fix the EDL before the Animatic Lock")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
