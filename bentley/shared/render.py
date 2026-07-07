#!/usr/bin/env python3
"""The ONE sanctioned way to render a Bentley character shot — bakes in the drift levers (SKILL §3a) so
they can't be forgotten:

  #4 BEST-OF keyframe pick   — pass `candidates` + `ref` and it ranks them (bentley.qa.image_bestof) and
                               renders from the top, on-model one (no seed exists, so this is the pick).
  #3 LAST-FRAME PIN          — pass `last_frame` and the clip is pinned first+last so it can't END off-model.
                               The mechanical drift_guard (in kie_client) REFUSES the render otherwise —
                               for a big-motion beat that must be first-frame-only, pass pin_override="reason".
  the @Bentley ELEMENT       — master + turnaround identity refs attached automatically.

Use this instead of hand-building a kie_client payload. `build_render(...)` is the pure payload builder
(no network — unit-tested); `render_shot(...)` adds best-of + hosting + the API call + download.

  from bentley.shared.render import render_shot
  render_shot(prompt, candidates=["c0.png","c1.png","c2.png"], ref=MASTER,
              last_frame="s7_end.png", out="renders/s7.mp4")            # best-of + pinned
  render_shot(prompt, first_frame="s8_key.png", pin_override="big play-leap; pin would warp",
              out="renders/s8.mp4")                                     # deliberate first-frame-only
"""
import os

from bentley.shared.kling import VIDEO_MODEL, bentley_element, i2v_payload

CD = "assets/character_design"
MASTER = f"{CD}/Bentley_MASTER_pixar.png"
TURNAROUND = f"{CD}/Bentley_MODEL_SHEET_turnaround.png"


def _is_url(s):
    return isinstance(s, str) and s.startswith(("http://", "https://"))


def build_render(prompt, first_url, *, last_url=None, master_url, turnaround_url,
                 element_desc=None, duration="5", aspect="16:9"):
    """Pure builder → (model, payload). No network. The drift_guard still runs at kie_client.run time."""
    els = [bentley_element(master_url, turnaround_url, description=element_desc)]
    payload = i2v_payload(prompt, first_url, last_url=last_url, elements=els,
                          duration=duration, aspect_ratio=aspect)
    return VIDEO_MODEL, payload


def pick_keyframe(candidates, ref):
    """Best-of #4: rank candidate keyframes vs the DNA reference, return the top path (+ prints ranking)."""
    from bentley.qa.image_bestof import rank
    rows = rank(candidates, ref)
    for i, r in enumerate(rows):
        print(f"  bestof #{i+1} score={r['score']:+.4f} {' '.join(r['flags'])} {r['path']}", flush=True)
    return rows[0]["path"]


def render_shot(prompt, *, first_frame=None, candidates=None, ref=None, last_frame=None,
                master=MASTER, turnaround=TURNAROUND, element_desc=None, duration="5", aspect="16:9",
                out=None, pin_override=None, timeout=1200, poll=10):
    """Render one Bentley shot with the drift levers baked in. Returns the kie_client result dict.

    first_frame: the picked keyframe (path or url). OR pass candidates+ref to best-of-pick it (#4).
    last_frame:  the on-model END keyframe (path or url) — pins the clip (#3). If omitted you MUST pass
                 pin_override="reason" (deliberate first-frame-only), else the guard refuses the render.
    """
    from bentley.shared import kie_client
    from bentley.shared.hosting import catbox_host

    if candidates:
        if not ref:
            raise ValueError("candidates given without ref — best-of needs the DNA reference image")
        first_frame = pick_keyframe(candidates, ref)
    if not first_frame:
        raise ValueError("provide first_frame, or candidates+ref to best-of-pick it")
    if last_frame is None and not pin_override:
        raise ValueError("no last_frame — pass an on-model end keyframe to pin the clip (drift lever #3), "
                         "or pin_override='reason' for a deliberate first-frame-only big-motion beat")

    host = lambda p: p if _is_url(p) else catbox_host(p)
    model, payload = build_render(
        prompt, host(first_frame), last_url=(host(last_frame) if last_frame else None),
        master_url=host(master), turnaround_url=host(turnaround),
        element_desc=element_desc, duration=duration, aspect=aspect)

    if pin_override and last_frame is None:
        os.environ["BENTLEY_PIN_OVERRIDE"] = pin_override   # the guard reads this + logs it
    try:
        r = kie_client.run(model, payload, timeout=timeout, poll=poll)
    finally:
        if pin_override and last_frame is None:
            os.environ.pop("BENTLEY_PIN_OVERRIDE", None)
    if out:
        kie_client.download(r["urls"][0], out)
        r["out"] = out
    return r
