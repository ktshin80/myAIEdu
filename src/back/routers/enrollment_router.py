from ..models.enrollment import EnrollRequest
from ..web.router import Response, Route


def build_routes(service):
    def enroll(request):
        req = EnrollRequest.from_payload(request.json())
        result = service.enroll(req)
        return Response(201, {"message": f"{req.name}님, {result.cohort.name} 수강 신청이 접수되었습니다."})

    return [Route("POST", "/api/enroll", enroll)]
