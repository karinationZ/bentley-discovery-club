"""Unit tests for the zero-credit Animatic Lock builder (bentley.episode_builder.animatic
+ bentley.episode_builder.placeholders).

These cover the PURE decision logic and the HARD credit guardrail — no media is rendered and
no API is called, so they run anywhere ffmpeg/PIL are installed (or even without them, since
nothing here shells out).

Run:  python tests/test_animatic.py     (or)  python -m pytest tests/test_animatic.py
"""
import os
import sys
import tempfile
from math import isclose

from bentley.episode_builder import animatic as A
from bentley.episode_builder import placeholders as P


# ---------------------------------------------------------------- credit guardrail (req #3)

def test_guard_allows_only_ffmpeg_and_ffprobe():
    # the two free, local media binaries are the ONLY thing the animatic path may shell out to
    assert P.assert_media_cmd(["ffmpeg", "-i", "x.mp4"]) is None
    assert P.assert_media_cmd(["ffprobe", "-show_entries", "format=duration"]) is None
    assert P.assert_media_cmd(["/opt/homebrew/bin/ffmpeg", "-y"]) is None   # abspath ok


def test_guard_blocks_credit_spending_commands():
    # anything that could spend KIE/fal/ElevenLabs credits or invoke the renderer is refused
    for bad in (["python", "pipeline.py", "shotlist.json"],
                ["python", "-m", "bentley.animation.render"],
                ["curl", "https://api.elevenlabs.io/v1/..."],
                ["kie", "generate"]):
        try:
            P.assert_media_cmd(bad)
        except P.CreditGuardError:
            continue
        raise AssertionError(f"guard let a credit-spending cmd through: {bad}")


def test_no_generation_module_is_imported_by_the_animatic_path():
    # importing the animatic must NOT transitively pull any module that can spend credits
    banned = ("bentley.animation", "bentley.asset_generation",
              "bentley.shared.kie_client", "bentley.shared.fal", "bentley.shared.eleven")
    loaded = [m for m in sys.modules if any(m == b or m.startswith(b + ".") for b in banned)]
    assert loaded == [], f"animatic path imported credit-spending modules: {loaded}"


# ---------------------------------------------------------------- VO parsing (req #1)

def test_vo_paths_extracts_every_mp3_line_in_order():
    # a beat may carry several recorded lines; all must be kept, in script order, prose stripped
    beat = {"vo": "scratch/ep2/vo/B_chase.mp3, scratch/ep2/vo/B_rude.mp3 (note: two lines)"}
    assert A.vo_paths(beat) == ["scratch/ep2/vo/B_chase.mp3", "scratch/ep2/vo/B_rude.mp3"]


def test_vo_paths_empty_when_no_vo():
    assert A.vo_paths({"type": "motion"}) == []


# ---------------------------------------------------------------- picture resolution

def _exists_set(paths):
    s = {os.path.normpath(p) for p in paths}
    return lambda p: os.path.normpath(p) in s


def test_existing_src_clip_is_reused():
    beat = {"id": "a3_19_hide", "type": "talk", "src": "scratch/ep2/talking/_indi_talk2.mp4"}
    kind, path = A.resolve_picture(beat, root=".", exists=_exists_set(["scratch/ep2/talking/_indi_talk2.mp4"]))
    assert kind == "reuse" and path.endswith("_indi_talk2.mp4")


def test_over_image_becomes_ken_burns_still():
    beat = {"id": "x", "type": "ffx", "over": "assets/character_design/TidePool_plate.jpg"}
    kind, path = A.resolve_picture(beat, root=".", exists=_exists_set(["assets/character_design/TidePool_plate.jpg"]))
    assert kind == "ken_burns" and path.endswith("TidePool_plate.jpg")


def test_keyframe_still_is_discovered_by_id():
    beat = {"id": "a0_02_boop", "type": "motion"}   # no src, but a same-named keyframe still exists
    kf = "assets/pilot_shots/ep2/keyframes"
    kind, path = A.resolve_picture(beat, root=".", keyframe_dir=kf,
                                   exists=_exists_set([f"{kf}/a0_02_boop.png"]))
    assert kind == "ken_burns" and path.endswith("a0_02_boop.png")


def test_missing_asset_falls_back_to_labeled_card():   # req #2 — never silently skip
    beat = {"id": "a0_05_title", "type": "card", "voice": "bentley", "asset": "brand template"}
    kind, path = A.resolve_picture(beat, root=".", keyframe_dir="nope", exists=lambda p: False)
    assert kind == "card" and path is None


# ---------------------------------------------------------------- audio resolution (req #1)

def test_vo_over_uses_the_recorded_mp3():
    beat = {"id": "a1_06_reintro", "type": "vo_over", "vo": "scratch/ep2/vo/N_intro.mp3"}
    kind, paths = A.resolve_audio(beat, root=".", exists=_exists_set(["scratch/ep2/vo/N_intro.mp3"]))
    assert kind == "files" and len(paths) == 1 and paths[0].endswith("N_intro.mp3")


def test_talk_clip_uses_its_embedded_recorded_line():
    beat = {"id": "a3_18_why", "type": "talk", "src": "scratch/ep2/talking/talk_B_why.mp4"}
    kind, src = A.resolve_audio(beat, root=".", exists=_exists_set(["scratch/ep2/talking/talk_B_why.mp4"]))
    assert kind == "embedded" and src.endswith("talk_B_why.mp4")


def test_silent_beat_when_no_line():
    beat = {"id": "a0_01_establish", "type": "ffx"}
    kind, val = A.resolve_audio(beat, root=".", exists=lambda p: False)
    assert kind == "silent" and val is None


# ---------------------------------------------------------------- duration policy

def test_beat_runs_long_enough_to_hold_its_whole_vo():
    # declared 4s but the recorded line is 6.2s -> the beat must stretch so no line is clipped
    assert isclose(A.beat_duration(4.0, 6.2, is_card=False), 6.2)
    assert A.vo_outlasts_beat(4.0, 6.2) is True


def test_declared_duration_wins_when_vo_is_shorter():
    assert isclose(A.beat_duration(5.0, 2.4, is_card=False), 5.0)
    assert A.vo_outlasts_beat(5.0, 2.4) is False


def test_silent_card_still_holds_a_readable_minimum():
    assert A.beat_duration(0.0, 0.0, is_card=True) >= 2.0


# ---------------------------------------------------------------- card labelling (req #2)

def test_card_label_names_speaker_and_beat():
    text, sub = A.card_label({"id": "a0_05_title", "type": "card", "voice": "bentley",
                              "note": "Title / channel ident."})
    assert "a0_05_title" in text
    assert "BENTLEY" in text.upper()
    assert sub   # a non-empty descriptor line


def test_card_label_falls_back_to_ref_then_dash():
    text, _ = A.card_label({"id": "a6_34_ants", "type": "motion", "ref": "indi"})
    assert "INDI" in text.upper() and "a6_34_ants" in text
    text2, _ = A.card_label({"id": "x_card", "type": "card"})
    assert "x_card" in text2   # no speaker known -> still names the beat


def test_card_label_title_is_renderable_ascii():
    # the caption font has no glyph for fancy separators (a middot renders as a tofu box) -> ASCII only
    text, _ = A.card_label({"id": "a4_27_breathe", "type": "talk", "voice": "bentley"})
    assert text.isascii(), f"card title has non-ASCII glyphs that won't render: {text!r}"


# ---------------------------------------------------------------- pure ffmpeg command builders

def test_ken_burns_cmd_is_a_zoompan_over_a_still():
    cmd = P.ken_burns_cmd("plate.jpg", 4.0, "out.mp4", w=1920, h=1080, fps=24)
    assert cmd[0] == "ffmpeg"
    joined = " ".join(cmd)
    assert "zoompan" in joined and "plate.jpg" in cmd and "out.mp4" == cmd[-1]
    assert P.assert_media_cmd(cmd) is None      # builder output passes the guard


def test_card_cmd_loops_a_png_for_the_duration():
    cmd = P.labeled_card_cmd("card.png", 3.0, "out.mp4", w=1920, h=1080, fps=24)
    assert cmd[0] == "ffmpeg" and "card.png" in cmd and cmd[-1] == "out.mp4"
    assert P.assert_media_cmd(cmd) is None


# ---------------------------------------------------------------- end-to-end plan (no rendering)

def test_resolve_beat_returns_a_complete_plan_for_every_beat():
    # a fully-unbuilt beat still yields a renderable plan (card + its recorded VO) — never skipped
    beat = {"id": "a1_06_reintro", "type": "vo_over", "vo": "scratch/ep2/vo/N_intro.mp3", "dur": "7"}
    plan = A.resolve_beat(beat, root=".", keyframe_dir="nope",
                          exists=_exists_set(["scratch/ep2/vo/N_intro.mp3"]))
    assert plan["id"] == "a1_06_reintro"
    assert plan["picture"][0] == "card"          # no clip/still -> labeled card
    assert plan["audio"][0] == "files"           # but the recorded narration is present
    assert plan["declared_dur"] == 7.0


# ---------------------------------------------------------------- shotlist schema audit

def test_audit_flags_label_style_vo():
    # the v3 pod schema put abstract VO IDs in `vo` (["P1_B01"]) — the animatic can't resolve those
    shots = [{"id": "p01_s03", "type": "performance", "vo": ["P1_I01", "P1_B03"]},
             {"id": "p02_s04", "type": "performance", "vo": "P2_I03"}]
    warns = A.audit_shotlist(shots)
    assert len(warns) == 2
    assert "p01_s03" in warns[0] and "p02_s04" in warns[1]


def test_audit_passes_path_style_vo():
    # real mp3 paths (and beats with no vo at all) are clean — no warnings
    shots = [{"id": "a1_06", "type": "vo_over", "vo": "scratch/ep2/vo/N_intro.mp3"},
             {"id": "a1_07", "type": "motion", "vo": "scratch/ep2/vo/B_chase.mp3, scratch/ep2/vo/B_rude.mp3"},
             {"id": "a0_03", "type": "motion"}]
    assert A.audit_shotlist(shots) == []


_TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]

if __name__ == "__main__":
    failed = 0
    for t in _TESTS:
        try:
            t()
            print(f"ok   {t.__name__}")
        except Exception as e:
            failed += 1
            print(f"FAIL {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(_TESTS) - failed}/{len(_TESTS)} passed")
    sys.exit(1 if failed else 0)
