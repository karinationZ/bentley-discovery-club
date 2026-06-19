"""Voice-placement scheduler shared by the mixer (mix.py) and the QA overlap-checker (qa/verify_sync.py).

Single source for the "one voice at a time" logic that verify_sync.py used to maintain as a
hand-kept copy of mix_v2_final.py ("MUST match mix_v2_final.py exactly"). Each caller still owns
its own event DATA; only the placement ALGORITHM is shared here.
"""


def make_next_talk_start(tljson, picdur):
    """Build f(after) -> start time of the first talk shot beginning after ``after`` (else picdur)."""
    def next_talk_start(after):
        c = [s["start"] for s in tljson if s["kind"] == "talk" and s["start"] > after + 0.05]
        return min(c) if c else picdur
    return next_talk_start


def place_sequential(events, next_talk_start, *, min_gap=0.25, pre_talk=0.2, min_cap=0.8):
    """Place voice events sequentially, one at a time.

    Each event starts at least ``min_gap`` after the previous placed voice ends, and is capped to
    end at least ``pre_talk`` before the next talk shot, so no two voices overlap and narration
    never collides with embedded dialogue.

    Args:
        events: iterable of ``(desired_start, duration, hardcap_or_None)``, PRE-SORTED by
            ``desired_start``.
        next_talk_start: callable ``f(after) -> float`` (see ``make_next_talk_start``).

    Yields:
        ``(index, start, cap, avail, placed)`` for every event in order. ``placed`` is True when
        ``cap >= min_cap``. Skipped events do NOT advance the clock (matching the original loop).
    """
    last_end = -10.0
    for i, (desired, duration, hardcap) in enumerate(events):
        start = max(desired, last_end + min_gap)
        avail = next_talk_start(start) - pre_talk - start
        cap = min(duration, avail)
        if hardcap is not None:
            cap = min(cap, hardcap)
        placed = cap >= min_cap
        if placed:
            last_end = start + cap
        yield i, start, cap, avail, placed
