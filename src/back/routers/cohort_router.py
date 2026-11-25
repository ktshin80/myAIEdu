from dataclasses import asdict

from ..web.router import Response, Route


def build_routes(service):
    def list_cohorts(request):
        return Response(200, [asdict(c) for c in service.list()])

    return [Route("GET", "/api/cohorts", list_cohorts)]
