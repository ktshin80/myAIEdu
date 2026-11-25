"""프레임워크 없는 최소 라우터와 요청/응답 값 객체. HTTP 서버 종류와 무관하다."""
import json
from dataclasses import dataclass
from typing import Any, Callable

from ..errors import ValidationError


@dataclass
class Request:
    method: str
    path: str
    query: dict
    read_body: Callable[[], bytes]

    def param(self, name, default=""):
        return self.query.get(name, [default])[0]

    def json(self):
        """본문을 JSON 객체(dict)로 읽는다. 형식이 아니면 ValidationError."""
        try:
            data = json.loads(self.read_body() or b"{}")
        except ValueError:
            raise ValidationError() from None
        if not isinstance(data, dict):
            raise ValidationError()
        return data


@dataclass
class Response:
    status: int
    body: Any


@dataclass(frozen=True)
class Route:
    method: str
    path: str
    handler: Callable[[Request], Response]


class Router:
    def __init__(self):
        self._routes = {}

    def include(self, routes):
        for r in routes:
            self._routes[(r.method, r.path)] = r.handler

    def resolve(self, method, path):
        return self._routes.get((method, path))
