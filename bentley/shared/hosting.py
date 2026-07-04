"""Public file hosting for model APIs.

Kling / Nano-Banana / Kling-Avatar / OmniHuman all require **public** image and audio URLs.
PRIMARY host: **KIE's own upload API** (tempfile.redpandaai.co) — guaranteed fetchable by every
KIE worker (catbox/tmpfiles URLs are refused by some worker pools, e.g. omnihuman: connection
reset), auth'd by KIE_KEY, 3-day retention (fine: inputs are consumed within minutes).
FALLBACK: catbox.moe (permanent, no auth) — NOTE catbox paused all uploads 2026-07-02
("storage issues"), and FLUX Kontext's fetcher can't pull catbox URLs anyway.
"""
import json
import os
import subprocess
from pathlib import Path


def kie_host(path):
    """Upload a local file to KIE's CDN and return its public downloadUrl (3-day retention)."""
    key = os.environ["KIE_KEY"]
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", "https://kieai.redpandaai.co/api/file-stream-upload",
         "-H", f"Authorization: Bearer {key}",
         "-F", f"file=@{path}", "-F", "uploadPath=bentley/assets",
         "-F", f"fileName={Path(path).name}"],
        capture_output=True, text=True)
    d = json.loads(r.stdout)
    if not d.get("success"):
        raise RuntimeError(f"KIE upload failed for {path}: {str(d)[:200]}")
    return d["data"]["downloadUrl"]


def catbox_host(path):
    """Host a file publicly. KIE CDN first (reliable for all KIE workers); catbox as fallback.

    Name kept for backward compatibility — every render script imports catbox_host."""
    try:
        return kie_host(path)
    except Exception:
        url = subprocess.check_output(
            ["curl", "-s", "-F", "reqtype=fileupload", "-F", f"fileToUpload=@{path}",
             "https://catbox.moe/user/api.php"]).decode().strip()
        if not url.startswith("http"):
            raise RuntimeError(f"both KIE and catbox upload failed for {path}: {url!r}")
        return url
