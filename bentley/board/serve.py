"""Local board server: serves the board (static) + a `/__open` endpoint that reveals a repo file in Finder.

Used by `python -m bentley.board serve <ep>` (and `make board-serve`). Clip/asset paths on board.html call
`/__open?path=<repo-relative>`, which runs `open -R <abspath>` (macOS reveal-in-Finder) — sandboxed to files
INSIDE the repo (a crafted `../` path or an out-of-repo path is refused). Without the server (plain file://),
the same links fall back to opening the file directly in the browser."""
import http.server
import os
import subprocess
import threading
import urllib.parse


def reveal(root, rel, opener=None):
    """Resolve a repo-relative path and reveal it in Finder. Returns (ok, message).

    SANDBOXED: refuses any path that resolves outside `root` (so a crafted `../` can't open system files).
    `opener` is injectable for testing; default runs `open -R <abspath>` (macOS reveal-in-Finder)."""
    root = os.path.abspath(root)
    target = os.path.abspath(os.path.join(root, rel or ""))
    if not (target == root or target.startswith(root + os.sep)):
        return False, "refused: path is outside the repo"
    if not os.path.exists(target):
        return False, "not found on disk"
    try:
        (opener or (lambda t: subprocess.run(["open", "-R", t], check=False)))(target)
    except Exception:
        return False, "open failed"
    return True, "revealed in Finder"


def _make_handler(root):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/__open"):
                return self._open()
            return super().do_GET()

        def _open(self):
            rel = (urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("path") or [""])[0]
            ok, msg = reveal(root, rel)
            self.send_response(200 if ok else 404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(msg.encode())

        def log_message(self, *args):
            pass   # quiet

    return Handler


def serve(ep, port=8713, open_browser=True, root=None):
    root = os.path.abspath(root or os.getcwd())
    os.chdir(root)
    url = f"http://localhost:{port}/episodes/{ep}/board.html"
    httpd = http.server.ThreadingHTTPServer(("localhost", port), _make_handler(root))
    print(f"Live board -> {url}")
    print("  · auto-updates every ~2s   · click any clip / asset path to reveal it in Finder   · Ctrl+C to stop")
    if open_browser:
        threading.Timer(1.0, lambda: subprocess.run(["open", url], check=False)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
    finally:
        httpd.server_close()
