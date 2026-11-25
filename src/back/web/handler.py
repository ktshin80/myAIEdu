"""http.server 어댑터. 요청을 Router에 넘기고 AppError를 JSON 응답으로 바꾼다."""
import json
import traceback
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from ..errors import AppError
from .router import Request, Response


def make_handler(router, static):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self._dispatch("GET")

        def do_POST(self):
            self._dispatch("POST")

        def _read_body(self):
            length = int(self.headers.get("Content-Length", 0))  # 잘못된 값이면 ValueError
            return self.rfile.read(length)

        def _dispatch(self, method):
            url = urlparse(self.path)
            route = router.resolve(method, url.path)
            if route is None:
                if method == "GET":
                    return self._send_static(url.path)
                return self._send_json(404, {"error": "없는 경로입니다."})
            request = Request(method, url.path, parse_qs(url.query), self._read_body)
            try:
                response = route(request)
            except AppError as e:
                response = Response(e.status, {"error": e.message})
            except Exception:
                traceback.print_exc()
                response = Response(500, {"error": "서버 오류가 발생했습니다."})
            self._send_json(response.status, response.body)

        def _send_json(self, code, body):
            self._send(code, "application/json; charset=utf-8",
                       json.dumps(body, ensure_ascii=False).encode("utf-8"))

        def _send_static(self, path):
            found = static.read(path)
            if found is None:
                return self._send_json(404, {"error": "찾을 수 없습니다."})
            self._send(200, *found)

        def _send(self, code, content_type, raw):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

    return Handler
