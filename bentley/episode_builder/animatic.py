#!/usr/bin/env python3
"""Animatic Lock builder — a ZERO-credit watchable cut of a whole episode from a JSON shotlist.

This is the tool the production rulebook requires before any Kling/KIE spend (Ep3+):
`.claude/skills/episode-production/SKILL.md` §10 step 4 + §9 "Animatic Lock". It composes ONLY
existing files — never a generation API — so it costs ZERO Kling/KIE/ElevenLabs credits:

  picture per beat  (in priority order)
    1. a reused approved clip          (`src`, or `over` when it points at a clip)
    2. a Ken-Burns still               (`over`/`still` image, or keyframes/<id>.png) — placeholders.ken_burns
    3. a labeled gray card             naming the speaking character + beat — placeholders.labeled_card
       (any beat with no shot yet falls back here; a beat is NEVER silently skipped)

  audio per beat
    - the recorded VO mp3s named in `vo` (ALL of them, in order), OR
    - the line embedded in a `talk` clip, OR
    - silence.
  Concatenated in shot order, the segments' audio IS "the complete recorded VO in script order"
  — assembled by CONCATENATING existing per-line mp3s, NEVER re-synthesised (TTS spends credits).

It reads the same `{id,type,dur,src,vo,over,status,...}` shotlist schema the cinematic-episode-writer
hands off (episode-production skill references/PRODUCTION_PLAYBOOK.md), so the animatic EDL can later graduate in place into
the final assemble (todo placeholders → rendered Kling clips).

HARD GUARDRAIL: every subprocess goes through ``placeholders.run_media`` (ffmpeg/ffprobe only). This
module imports NOTHING from ``bentley.animation`` / ``bentley.asset_generation`` / the KIE/fal/eleven
clients, and never calls ``pipeline.produce()``. (Enforced by tests/test_animatic.py.)

Run:  PYTHONPATH=. python -m bentley.episode_builder.animatic episodes/ep2/shotlists/ep2_master.json
"""
import argparse
import json
import os
import re
import subprocess

from bentley.shared.ffio import dur as media_dur
from bentley.shared.paths import ROOT
from bentley.episode_builder import placeholders as P

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
SPEAKERS = {"bentley": "BENTLEY", "indi": "INDI", "pip": "PIP",
            "narrator": "NARRATOR", "theo": "NARRATOR", "bill": "NARRATOR"}


# ============================================================ pure decision logic (unit-tested)

def parse_dur(v, default=0.0):
    """Beat duration as a float; tolerates strings like ``"5"`` / ``"4.5"`` / ``"editorial"``."""
    try:
        return float(str(v).strip().split()[0])
    except (ValueError, IndexError, AttributeError):
        return float(default)


def vo_paths(beat):
    """Every recorded-line mp3 named in the beat's ``vo`` field, in order, prose stripped.

    A beat may carry several lines (e.g. ``"B_chase.mp3, B_rude.mp3 (two lines)"``) — keep them ALL
    so no recorded line is dropped from the script-order VO reel.
    """
    raw = beat.get("vo")
    if not raw:
        return []
    return re.findall(r"[^\s,]+\.mp3", str(raw))


def _abs(root, p):
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(root, p))


def _ext(p):
    return os.path.splitext(p)[1].lower()


def resolve_picture(beat, *, root=".", keyframe_dir=None, exists=os.path.exists):
    """Decide the placeholder picture for a beat. Returns ``(kind, path|None)`` where kind is
    ``"reuse"`` (existing clip), ``"ken_burns"`` (existing still), or ``"card"`` (no asset)."""
    src = beat.get("src")
    if src:
        ap = _abs(root, src)
        if exists(ap):
            return ("ken_burns" if _ext(ap) in IMAGE_EXT else "reuse", ap)

    over = beat.get("over")                       # may be a clip path, a still path, or a shot-id ref
    if over and ("/" in str(over) or _ext(str(over)) in VIDEO_EXT | IMAGE_EXT):
        ap = _abs(root, over)
        if exists(ap):
            return ("ken_burns" if _ext(ap) in IMAGE_EXT else "reuse", ap)

    still = beat.get("still")
    if still:
        ap = _abs(root, still)
        if exists(ap):
            return ("ken_burns", ap)

    if keyframe_dir:                              # a same-named keyframe still is the beat's planned frame
        kp = _abs(root, os.path.join(keyframe_dir, f"{beat.get('id', '')}.png"))
        if exists(kp):
            return ("ken_burns", kp)

    return ("card", None)                         # never skip — labeled card naming speaker + beat


def resolve_audio(beat, *, root=".", exists=os.path.exists):
    """Decide the beat's audio. Returns ``("files", [mp3,...])`` (recorded VO lines, in order),
    ``("embedded", clip)`` (the line baked into a talk clip), or ``("silent", None)``."""
    present = [_abs(root, p) for p in vo_paths(beat) if exists(_abs(root, p))]
    if present:
        return ("files", present)
    if beat.get("type") == "talk":
        src = beat.get("src")
        if src and exists(_abs(root, src)):
            return ("embedded", _abs(root, src))
    return ("silent", None)


def card_label(beat):
    """``(title, subtitle)`` for a labeled card: ``"SPEAKER · beat-id"`` + a short descriptor."""
    spk = beat.get("voice") or beat.get("ref")
    name = SPEAKERS.get(str(spk).lower(), str(spk).upper()) if spk else ""
    bid = beat.get("id", "?")
    title = f"{name} - {bid}" if name else f"{bid}"   # ASCII separator (caption font lacks middot)
    sub = beat.get("line") or beat.get("note") or beat.get("keyframe") or beat.get("asset") \
        or beat.get("type", "")
    sub = re.sub(r"\s+", " ", str(sub)).strip()
    if len(sub) > 90:
        sub = sub[:87] + "..."
    return title, sub


def beat_duration(declared, audio_dur, *, is_card, min_card=2.0):
    """The beat must hold its whole VO — so it runs for at least as long as its recorded line."""
    d = max(float(declared), float(audio_dur))
    if is_card:
        d = max(d, min_card)
    return d


def vo_outlasts_beat(declared, audio_dur, eps=0.05):
    """True when the recorded VO is longer than the planned shot — a timing flag for QA."""
    return float(audio_dur) > float(declared) + eps


def audit_shotlist(shots):
    """Warn about beats in the abstract pod/label schema the animatic can't resolve.

    The old v3 handoff put VO *labels/IDs* in ``vo`` (e.g. ``["P1_B01"]``) instead of mp3 paths, which
    silently degrades every line to a blank card. Returns human-readable warnings (empty when clean).
    """
    warnings = []
    for b in shots:
        raw = b.get("vo")
        if raw and not vo_paths(b):
            warnings.append(f"{b.get('id', '?')}: vo={raw!r} has no .mp3 path "
                            f"(label/pod schema? -> this line becomes a SILENT card)")
    return warnings


def resolve_beat(beat, *, root=".", keyframe_dir=None, exists=os.path.exists):
    """Full placeholder plan for one beat (picture + audio + declared duration)."""
    return {
        "id": beat.get("id"),
        "type": beat.get("type"),
        "declared_dur": parse_dur(beat.get("dur"), 0.0),
        "picture": resolve_picture(beat, root=root, keyframe_dir=keyframe_dir, exists=exists),
        "audio": resolve_audio(beat, root=root, exists=exists),
        "beat": beat,
    }


# ============================================================ media build (ffmpeg only)

def _has_audio(path):
    r = P.run_media(["ffprobe", "-v", "error", "-select_streams", "a",
                     "-show_entries", "stream=index", "-of", "csv=p=0", path],
                    capture_output=True, text=True, check=False)
    return bool(r.stdout.strip())


def _safe_dur(path):
    try:
        return media_dur(path)
    except (subprocess.CalledProcessError, ValueError):
        return 0.0


def measure_audio(audio_plan):
    """Total recorded-audio length for a beat's audio plan (0.0 if silent)."""
    kind, val = audio_plan
    if kind == "files":
        return sum(_safe_dur(p) for p in val)
    if kind == "embedded":
        return _safe_dur(val) if _has_audio(val) else 0.0
    return 0.0


def _build_picture(plan, beat_dur, out_video):
    """Render the beat's placeholder picture (video-only) to ``out_video``."""
    kind, src = plan["picture"]
    if kind == "reuse":
        native = _safe_dur(src)
        pad = max(0.0, beat_dur - native)
        chain = f"[0:v]{P.NORM}"
        if pad > 0.02:                                   # clip shorter than the beat -> hold last frame
            chain += f",tpad=stop_mode=clone:stop_duration={pad:.3f}"
        chain += f",trim=0:{beat_dur:.3f},setpts=PTS-STARTPTS[v]"
        P.run_media(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", chain,
                     "-map", "[v]", "-an", "-t", f"{beat_dur:.3f}"] + P.VENC + [out_video])
    elif kind == "ken_burns":
        P.ken_burns(src, beat_dur, out_video)
    else:                                                # card
        title, sub = card_label(plan["beat"])
        P.labeled_card(title, sub, beat_dur, out_video)
    return out_video


def _build_segment(picture_video, audio_plan, beat_dur, out):
    """Mux the beat's audio (recorded VO / embedded line / silence) over its placeholder picture."""
    kind, val = audio_plan
    inputs, af, amap = ["-i", picture_video], None, "1:a"
    if kind == "files":
        for p in val:
            inputs += ["-i", p]
        if len(val) == 1:
            af = f"[1:a]aresample=48000,apad,atrim=0:{beat_dur:.3f},asetpts=PTS-STARTPTS[a]"
        else:
            cc = "".join(f"[{i + 1}:a]" for i in range(len(val)))
            af = (f"{cc}concat=n={len(val)}:v=0:a=1,aresample=48000,apad,"
                  f"atrim=0:{beat_dur:.3f},asetpts=PTS-STARTPTS[a]")
        amap = "[a]"
    elif kind == "embedded" and _has_audio(val):
        inputs += ["-i", val]
        af = f"[1:a]aresample=48000,apad,atrim=0:{beat_dur:.3f},asetpts=PTS-STARTPTS[a]"
        amap = "[a]"
    else:                                                # silent (no line, or embedded clip had no audio)
        inputs += ["-f", "lavfi", "-t", f"{beat_dur:.3f}",
                   "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    cmd = ["ffmpeg", "-y", "-loglevel", "error"] + inputs
    if af:
        cmd += ["-filter_complex", af]
    cmd += ["-map", "0:v", "-map", amap, "-c:v", "copy"] + P.AENC + ["-t", f"{beat_dur:.3f}", out]
    P.run_media(cmd)
    return out


# ============================================================ orchestration

def _guess_ep(shotlist_path, data):
    m = re.search(r"(ep\d+)", str(shotlist_path), re.I)
    if m:
        return m.group(1).lower()
    ep = str(data.get("_meta", {}).get("episode", ""))
    m = re.search(r"episode\s*(\d+)", ep, re.I)
    return f"ep{m.group(1)}" if m else "ep"


def build_animatic(shotlist_path, out_path=None, ep=None, keyframe_dir=None, workdir=None,
                   runtime_target=None):
    """Build one ``*_ANIMATIC.mp4`` for the whole episode. Returns ``(out_path, runtime, report)``."""
    data = json.load(open(shotlist_path))
    shots = data.get("shots", [])
    root = str(ROOT)
    ep = ep or _guess_ep(shotlist_path, data)

    schema_warnings = audit_shotlist(shots)
    if "pods" in data:
        schema_warnings.insert(0, "shotlist has a top-level 'pods' key — looks like the abstract "
                                  "v3 pod schema; the animatic needs the file-path schema "
                                  "(episodes/<ep>/shotlists/<ep>_master.json).")
    if schema_warnings:
        print("\n" + "!" * 64)
        print(f"SCHEMA WARNING — {len(schema_warnings)} beat(s) won't resolve their VO from this shotlist:")
        for w in schema_warnings[:12]:
            print(f"  ! {w}")
        if len(schema_warnings) > 12:
            print(f"  ! ...and {len(schema_warnings) - 12} more")
        print("  Fix at the source (cinematic-episode-writer must emit mp3 PATHS, not VO labels/IDs).")
        print("!" * 64 + "\n")
    if keyframe_dir is None:
        kd = f"assets/pilot_shots/{ep}/keyframes"
        keyframe_dir = kd if os.path.isdir(_abs(root, kd)) else None
    out_path = _abs(root, out_path or f"episodes/{ep}/{ep.upper()}_ANIMATIC.mp4")
    workdir = _abs(root, workdir or f"episodes/{ep}/animatic_work")
    runtime_target = runtime_target or data.get("_meta", {}).get("runtime_target_seconds")
    os.makedirs(workdir, exist_ok=True)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    timeline, segs, vo_reel, overruns = [], [], [], []
    counts = {"reuse": 0, "ken_burns": 0, "card": 0}
    t = 0.0
    print(f"{'#':>2}  {'id':22s} {'picture':10s} {'audio':9s} {'dur':>6s} {'start':>7s}")
    for i, beat in enumerate(shots):
        plan = resolve_beat(beat, root=root, keyframe_dir=keyframe_dir)
        a_kind = plan["audio"][0]
        a_dur = measure_audio(plan["audio"])
        is_card = plan["picture"][0] == "card"
        bd = beat_duration(plan["declared_dur"], a_dur, is_card=is_card)

        pic = os.path.join(workdir, f"{i:02d}_{plan['id']}_pic.mp4")
        seg = os.path.join(workdir, f"{i:02d}_{plan['id']}.mp4")
        _build_picture(plan, bd, pic)
        _build_segment(pic, plan["audio"], bd, seg)
        segs.append(seg)
        counts[plan["picture"][0]] += 1

        if a_kind == "files":
            vo_reel += [os.path.relpath(p, root) for p in plan["audio"][1]]
        elif a_kind == "embedded":
            vo_reel.append(os.path.relpath(plan["audio"][1], root) + " (embedded line)")
        if vo_outlasts_beat(plan["declared_dur"], a_dur):
            overruns.append((plan["id"], plan["declared_dur"], round(a_dur, 2)))

        timeline.append({
            "id": plan["id"], "start": round(t, 3), "dur": round(bd, 3),
            "kind": "talk" if plan["type"] == "talk" else "motion",   # scheduler-compatible (mix.py)
            "type": plan["type"], "status": beat.get("status"),
            "picture": plan["picture"][0],
            "src": os.path.relpath(plan["picture"][1], root) if plan["picture"][1] else None,
            "audio": a_kind, "vo_outlasts_beat": vo_outlasts_beat(plan["declared_dur"], a_dur),
        })
        print(f"{i:>2}  {plan['id']:22s} {plan['picture'][0]:10s} {a_kind:9s} {bd:6.2f} {t:7.2f}")
        t += bd

    lst = os.path.join(workdir, "concat.txt")
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    P.run_media(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                 "-i", lst, "-c", "copy", out_path])

    tl_path = out_path.rsplit(".", 1)[0] + "_timeline.json"
    json.dump({"animatic": os.path.relpath(out_path, root), "shotlist": os.path.relpath(shotlist_path, root),
               "runtime_s": round(t, 2), "counts": counts, "vo_reel": vo_reel,
               "vo_outlasts_beat": overruns, "schema_warnings": schema_warnings, "shots": timeline},
              open(tl_path, "w"), indent=1)

    report = {"out": out_path, "timeline": tl_path, "runtime_s": round(t, 2),
              "counts": counts, "n_shots": len(shots), "n_vo_lines": len(vo_reel),
              "overruns": overruns, "runtime_target": runtime_target,
              "schema_warnings": schema_warnings, "media_calls": dict(P.MEDIA_CALLS)}
    _print_report(report)
    return out_path, t, report


def _print_report(r):
    print("\n" + "=" * 64)
    print(f"ANIMATIC -> {r['out']}")
    print(f"  runtime        {r['runtime_s']:.1f}s ({r['runtime_s'] / 60:.2f} min)"
          + (f"   target {r['runtime_target']}" if r["runtime_target"] else ""))
    print(f"  beats          {r['n_shots']}  "
          f"(reuse {r['counts']['reuse']} · ken-burns {r['counts']['ken_burns']} · card {r['counts']['card']})")
    print(f"  VO lines       {r['n_vo_lines']} concatenated in script order"
          + (f"   ⚠ {len(r['schema_warnings'])} unresolved-VO beats (see SCHEMA WARNING above)"
             if r["schema_warnings"] else ""))
    if r["overruns"]:
        print(f"  VO OUTLASTS BEAT ({len(r['overruns'])}) — re-time before render:")
        for bid, dec, ad in r["overruns"]:
            print(f"      {bid:22s} planned {dec}s  vo {ad}s")
    else:
        print("  VO outlasts beat: none")
    print(f"  subprocess     {r['media_calls']}  (ffmpeg/ffprobe only)")
    print("  CREDITS SPENT: 0 — no KIE/fal/ElevenLabs; no generation module; existing files only.")
    print("=" * 64)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build a zero-credit episode animatic from a JSON shotlist.")
    ap.add_argument("shotlist", help="path to episodes/<ep>/shotlists/*.json")
    ap.add_argument("--out", help="output mp4 (default episodes/<ep>/<EP>_ANIMATIC.mp4)")
    ap.add_argument("--ep", help="episode tag, e.g. ep2 (default: inferred from the path)")
    ap.add_argument("--keyframes", help="keyframe-still dir (default assets/pilot_shots/<ep>/keyframes)")
    ap.add_argument("--workdir", help="scratch dir for per-beat segments")
    args = ap.parse_args(argv)
    build_animatic(args.shotlist, out_path=args.out, ep=args.ep,
                   keyframe_dir=args.keyframes, workdir=args.workdir)


if __name__ == "__main__":
    main()
