"""EDL lint (bentley/qa/edl_lint.py) — mechanical freeze-push / coverage checks.
Verifies: VO-outlasts-picture FAILs, over-retime FAILs, legal retime WARNs, missing vo mp3 FAILs,
same-clip back-to-back FAILs, todo pieces only INFO, and a clean EDL passes."""
import json
import shutil
import subprocess

import numpy as np
import pytest
from PIL import Image

from bentley.qa.edl_lint import lint, main

pytestmark = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg required")


def make_mp3(path, seconds):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                    "-i", f"sine=frequency=440:duration={seconds}", "-c:a", "libmp3lame",
                    str(path)], check=True)
    return str(path)


def make_clip(tmp_path, name, seconds, fps=12):
    fd = tmp_path / f"{name}_frames"
    fd.mkdir()
    for i in range(int(seconds * fps)):
        arr = np.full((64, 64, 3), 30, np.uint8)
        arr[20:36, 4 + (i * 3) % 40:16 + (i * 3) % 40] = 220
        Image.fromarray(arr).save(fd / f"f{i:05d}.png")
    out = str(tmp_path / f"{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
                    "-i", str(fd / "f%05d.png"), "-c:v", "libx264", "-crf", "12",
                    "-pix_fmt", "yuv420p", out], check=True)
    return out


def write_list(tmp_path, shots):
    p = tmp_path / "list.json"
    p.write_text(json.dumps({"shots": shots}))
    return str(p)


def test_vo_outlasting_picture_fails(tmp_path):
    vo = make_mp3(tmp_path / "line.mp3", 2.0)
    sl = write_list(tmp_path, [{"id": "s1", "dur": 1.0, "vo": vo, "scale": "wide",
                                "seq": [{"dur": 1.0, "scale": "wide", "sync": "vo-over-alive"}]}])
    fails, warns, infos = lint(sl, root=str(tmp_path))
    assert any("outlasts picture" in f for f in fails)


def test_covered_vo_passes(tmp_path):
    vo = make_mp3(tmp_path / "line2.mp3", 1.0)
    sl = write_list(tmp_path, [{"id": "s1", "dur": 1.5, "vo": vo, "scale": "wide",
                                "seq": [{"dur": 1.5, "scale": "wide", "sync": "vo-over-alive"}]}])
    fails, warns, infos = lint(sl, root=str(tmp_path))
    assert not fails


def test_over_retime_fails_legal_retime_warns(tmp_path):
    clip = make_clip(tmp_path, "c1", 1.0)
    over = write_list(tmp_path, [{"id": "s1", "scale": "wide",
                                  "seq": [{"src": clip, "dur": 2.0, "scale": "wide"}]}])
    fails, _, _ = lint(over, root=str(tmp_path))
    assert any("push=" in f and "don't stretch" in f for f in fails)

    legal = write_list(tmp_path, [{"id": "s1", "scale": "wide",
                                   "seq": [{"src": clip, "dur": 1.2, "scale": "wide"}]}])
    fails, warns, _ = lint(legal, root=str(tmp_path))
    assert not fails and any("retime x" in w for w in warns)


def test_missing_vo_mp3_fails(tmp_path):
    sl = write_list(tmp_path, [{"id": "s1", "dur": 2.0, "vo": "vo/never_recorded.mp3",
                                "scale": "wide", "seq": [{"dur": 2.0, "scale": "wide", "sync": "-"}]}])
    fails, _, _ = lint(sl, root=str(tmp_path))
    assert any("vo mp3 missing" in f for f in fails)


def test_same_clip_back_to_back_fails(tmp_path):
    clip = make_clip(tmp_path, "c2", 2.0)
    sl = write_list(tmp_path, [{"id": "s1", "scale": "wide",
                                "seq": [{"src": clip, "dur": 1.0, "scale": "wide"},
                                        {"src": clip, "dur": 1.0, "scale": "wide"}]}])
    fails, _, _ = lint(sl, root=str(tmp_path))
    assert any("back-to-back" in f for f in fails)


def test_todo_pieces_are_info_not_fail(tmp_path):
    sl = write_list(tmp_path, [{"id": "s1", "status": "todo", "scale": "wide",
                                "seq": [{"plan": "kling", "dur": 5.0, "scale": "wide",
                                         "sync": "vo-over-alive"}]}])
    fails, warns, infos = lint(sl, root=str(tmp_path))
    assert not fails and any("todo" in i for i in infos)


def test_main_exit_codes(tmp_path):
    vo = make_mp3(tmp_path / "line3.mp3", 2.0)
    bad = write_list(tmp_path, [{"id": "s1", "dur": 0.5, "vo": vo, "scale": "wide",
                                 "seq": [{"dur": 0.5, "scale": "wide", "sync": "-"}]}])
    assert main([bad, "--root", str(tmp_path)]) == 1
    ok = write_list(tmp_path, [{"id": "s1", "dur": 3.0, "vo": vo, "scale": "wide",
                                "seq": [{"dur": 3.0, "scale": "wide", "sync": "-"}]}])
    assert main([ok, "--root", str(tmp_path)]) == 0
