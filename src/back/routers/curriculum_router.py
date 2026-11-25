from dataclasses import asdict

from ..web.router import Response, Route


def build_routes(service):
    def list_curriculum(request):
        items = service.list(request.param("track"))
        return Response(200, [asdict(i) for i in items])

    return [Route("GET", "/api/curriculum", list_curriculum)]
