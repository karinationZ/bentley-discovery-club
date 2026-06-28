"""Public file hosting for model APIs.

Kling / Nano-Banana / Kling-Avatar all require **public** image and audio URLs. catbox.moe is the
canonical host: permanent, no auth, works for the KIE jobs API. (Gotcha: FLUX Kontext's fetcher
cannot pull catbox URLs — host FLUX inputs on tmpfiles instead. See kie-ai-integration notes.)
"""
import subprocess


def catbox_host(path):
    """Upload a local file to catbox.moe and return its public URL."""
    url = subprocess.check_output(
        ["curl", "-s", "-F", "reqtype=fileupload", "-F", f"fileToUpload=@{path}",
         "https://catbox.moe/user/api.php"]).decode().strip()
    if not url.startswith("http"):
        raise RuntimeError(f"catbox upload failed for {path}: {url!r}")
    return url
