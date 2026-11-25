import os

MIME = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8"}


class StaticFiles:
    def __init__(self, root):
        self.root = os.path.realpath(root)

    def read(self, url_path):
        """(MIME, 바이트)를 돌려준다. 없거나 root 밖이면 None."""
        rel = "index.html" if url_path in ("", "/") else url_path.lstrip("/")
        full = os.path.realpath(os.path.join(self.root, rel))
        # root 밖 경로 접근(../)을 막는다.
        if not full.startswith(self.root + os.sep) or not os.path.isfile(full):
            return None
        with open(full, "rb") as f:
            raw = f.read()
        return MIME.get(os.path.splitext(full)[1], "application/octet-stream"), raw
