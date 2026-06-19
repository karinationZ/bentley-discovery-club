"""Unit tests for the extracted voice-placement scheduler (bentley.episode_builder.timeline).

Verifies the algorithm shared by mix.py and qa/verify_sync.py against hand-computed expected
values, with synthetic timeline data (no media / no API calls needed).

Run:  .venv/bin/python -m pytest tests/test_timeline.py     (or)  .venv/bin/python tests/test_timeline.py
"""
from math import isclose

from bentley.episode_builder.timeline import make_next_talk_start, place_sequential


def test_next_talk_start():
    tl = [{"id": "m1", "start": 0.0, "kind": "motion"},
          {"id": "t1", "start": 5.0, "kind": "talk"},
          {"id": "t2", "start": 15.0, "kind": "talk"}]
    nts = make_next_talk_start(tl, picdur=18.0)
    assert isclose(nts(0.0), 5.0)
    assert isclose(nts(5.0), 15.0)     # strictly after 5.0 + 0.05
    assert isclose(nts(15.0), 18.0)    # none left -> picdur


def test_place_sequential_caps_and_hardcap():
    tl = [{"start": 0.0, "kind": "motion"}, {"start": 5.0, "kind": "talk"},
          {"start": 9.0, "kind": "motion"}, {"start": 15.0, "kind": "talk"}]
    nts = make_next_talk_start(tl, picdur=18.0)
    # (desired, duration, hardcap) pre-sorted by desired
    events = [(0.4, 3.0, None), (9.3, 10.0, None), (9.5, 1.5, 1.0)]
    placed = [(i, round(s, 3), round(c, 3)) for i, s, c, _a, ok in place_sequential(events, nts) if ok]
    assert placed == [(0, 0.4, 3.0),    # capped by duration
                      (1, 9.3, 5.5),    # capped by next talk (15.0 - 0.2 - 9.3)
                      (2, 15.05, 1.0)]  # min_gap pushes start; hardcap 1.0 wins over 2.75 window


def test_skip_does_not_advance_clock():
    tl = [{"start": 0.0, "kind": "motion"}, {"start": 5.0, "kind": "talk"},
          {"start": 8.0, "kind": "motion"}, {"start": 13.0, "kind": "talk"}]
    nts = make_next_talk_start(tl, picdur=15.0)
    events = [(4.5, 2.0, None),   # window only 0.3s -> skipped
              (8.3, 1.0, None)]   # must start at its own desired 8.3 (skipped event didn't move the clock)
    out = list(place_sequential(events, nts))
    assert out[0][4] is False                       # first skipped
    assert out[1][4] is True and isclose(out[1][1], 8.3)


if __name__ == "__main__":
    test_next_talk_start()
    test_place_sequential_caps_and_hardcap()
    test_skip_does_not_advance_clock()
    print("ok: all timeline scheduler tests passed")
