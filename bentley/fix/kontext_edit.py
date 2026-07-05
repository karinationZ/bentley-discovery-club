#!/usr/bin/env python3
"""Kontext Edit — the sanctioned SURGICAL-AI-EDIT tier of the fix-first ladder, productionized.

Pattern proven on the s10a googly-eye fix (scratch/ep4/fix_s10a_eyes.py, owner-approved 2026-07-05):
to change an otherwise-APPROVED frame, FLUX Kontext edits it with a minimal-change prompt — never a
regeneration from masters (regeneration drifts the approved style; owner law). This wrapper stops
that boilerplate (tmpfiles hosting + polling + download) being rewritten per episode.

⚖️ SPENDS KIE CREDITS (image tier, a few cr/call). It sits ABOVE the zero-token layers in the
fix-first ladder: try the edit layer (edl_lint / tail_trim / assembler) and the pixel layer
(magic_wand) first; come here for defects those can't own — anatomy-level drift on a keyframe
(too-long tail, googly eyes, a mangled prop) where the staging is otherwise approved.

Usage:
  KIE_KEY=... PYTHONPATH=. python -m bentley.fix.kontext_edit IMG --prompt "Fix ONLY ..." \
      [--out OUT] [--model flux-kontext-max] [--aspect 16:9]

Prompt discipline (what made s10a work): name the ONE defect ("Fix ONLY the puppy's eyes ..."),
describe the canon-correct result, and END with "keep her face structure, fur, body, pose and the
entire rest of the image EXACTLY the same." After the edit, re-run the SAME QC the frame failed
(paw-zoom / eye-zoom / master side-by-side) — an unverified fix is not a fix.

FLUX gotcha: inputs are hosted on tmpfiles.org — the FLUX fetcher can't pull catbox/KIE-CDN URLs.
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request

GEN = "https://api.kie.ai/api/v1/flux/kontext/generate"
REC = "https://api.kie.ai/api/v1/flux/kontext/record-info?taskId={}"
TIMEOUT_S = 240


def default_out(path):
    stem, _ = os.path.splitext(path)
    return f"{stem}_kontext.png"


def tmpfiles_dl_url(url):
    """tmpfiles page URL -> direct-download URL (the form the FLUX fetcher can read)."""
    if "tmpfiles.org/dl/" in url:
        return url
    return url.replace("tmpfiles.org/", "tmpfiles.org/dl/", 1)


def host_tmpfiles(path):
    out = subprocess.check_output(["curl", "-s", "-F", f"file=@{path}",
                                   "https://tmpfiles.org/api/v1/upload"]).decode()
    return tmpfiles_dl_url(json.loads(out)["data"]["url"])


def _post(url, body, key):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {key}",
                                          "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


def _get(url, key):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    return json.load(urllib.request.urlopen(req))


def kontext_edit(image, prompt, out=None, model="flux-kontext-max", aspect="16:9"):
    key = os.environ.get("KIE_KEY")
    if not key:
        raise SystemExit("KIE_KEY not set — this tool spends KIE image credits and needs the key")
    out = out or default_out(image)
    src_url = host_tmpfiles(image)
    print(f"hosted: {src_url}", flush=True)
    r = _post(GEN, {"prompt": prompt, "inputImage": src_url, "model": model,
                    "aspectRatio": aspect, "outputFormat": "png"}, key)
    tid = r["data"]["taskId"]
    print(f"taskId: {tid}", flush=True)
    t0 = time.time()
    while time.time() - t0 < TIMEOUT_S:
        d = _get(REC.format(tid), key)["data"]
        flag = d.get("successFlag")
        if flag == 1:
            url = d["response"]["resultImageUrl"]
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp, open(out, "wb") as f:
                f.write(resp.read())
            print(f"KONTEXT EDIT DONE -> {out}", flush=True)
            return out
        if flag in (2, 3):
            raise RuntimeError(f"flux kontext failed (flag {flag}) — fix the prompt/input, "
                               f"don't blind-retry")
        time.sleep(6)
    raise TimeoutError(f"taskId {tid} still pending after {TIMEOUT_S}s")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Surgical FLUX Kontext edit of an approved frame "
                                             "(SPENDS KIE image credits)")
    ap.add_argument("image")
    ap.add_argument("--prompt", required=True,
                    help='minimal-change edit: "Fix ONLY <defect> ... keep the rest EXACTLY the same"')
    ap.add_argument("--out")
    ap.add_argument("--model", default="flux-kontext-max")
    ap.add_argument("--aspect", default="16:9")
    a = ap.parse_args(argv)
    kontext_edit(a.image, a.prompt, a.out, a.model, a.aspect)
    return 0


if __name__ == "__main__":
    sys.exit(main())
