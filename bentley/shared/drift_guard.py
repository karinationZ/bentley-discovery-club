#!/usr/bin/env python3
"""Drift-safety guard — mechanically REFUSES an un-pinned character video render (drift lever #3).

Wired into `kie_client.run()` right after the Animatic-Lock spend guard, so it catches EVERY render
path — the sanctioned `bentley.shared.render.render_shot`, an old scratch script, or a raw
`kie_client.run(...)` an agent hand-writes. A "character shot" (a Kling VIDEO render carrying a
`kling_elements` identity element) MUST pin the last frame (`image_urls` has ≥2 entries: first + last),
so the clip cannot END on a mutated Bentley (the s7b failure). This turns "documented default" into a
mechanical lock — the same pattern as `bentley/shared/gates.py`.

Escape hatch (a DELIBERATE choice, not silent omission): for a big-motion beat where last-frame pinning
would warp the interpolation, set `BENTLEY_PIN_OVERRIDE="<reason>"` — the render proceeds first-frame-only
with a loud stderr banner (the reason is logged, so the choice is on the record). Environment/plate shots
(no `kling_elements`) are not character shots and are never gated.
"""
import os
import sys


def _is_character_video(model, inp):
    """True for a Kling VIDEO render that carries a character identity element."""
    m = (model or "").lower()
    if not ("kling" in m and "video" in m):
        return False
    return bool(inp.get("kling_elements"))


def assert_pin_ok(model, inp):
    """Raise PermissionError if a character video shot is not last-frame-pinned (unless overridden)."""
    if not _is_character_video(model, inp):
        return
    if len(inp.get("image_urls") or []) >= 2:
        return  # first + last frame present → pinned
    reason = os.environ.get("BENTLEY_PIN_OVERRIDE")
    if reason:
        print(f"⚠️  DRIFT-PIN OVERRIDE — character shot rendered FIRST-FRAME-ONLY. Reason: {reason}",
              file=sys.stderr, flush=True)
        return
    raise PermissionError(
        "DRIFT GUARD (SKILL §3a lever #3): this character video shot is NOT last-frame-pinned.\n"
        "  Pass a 2-element image_urls [first, last] — easiest via "
        "bentley.shared.kling.i2v_payload(prompt, first, last_url=<on-model end keyframe>, elements=[...]) "
        "or bentley.shared.render.render_shot(..., last_frame=...).\n"
        "  For a deliberate big-motion beat that must render first-frame-only, set "
        "BENTLEY_PIN_OVERRIDE=\"<reason>\" — never to route around drift, only when pinning would warp.")
