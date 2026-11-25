"""조립 지점(composition root). 구현체를 만들어 서로 연결하는 일은 여기서만 한다."""
from http.server import ThreadingHTTPServer

from . import config
from .db.database import Database
from .routers import cohort_router, curriculum_router, enrollment_router
from .services.cohort_service import CohortService
from .services.curriculum_service import CurriculumService
from .services.enrollment_service import EnrollmentService
from .web.handler import make_handler
from .web.router import Router
from .web.static import StaticFiles


def build_router(database):
    router = Router()
    router.include(curriculum_router.build_routes(CurriculumService(database)))
    router.include(cohort_router.build_routes(CohortService(database)))
    router.include(enrollment_router.build_routes(EnrollmentService(database)))
    return router


def create_server(database, host=config.HOST, port=config.PORT):
    handler = make_handler(build_router(database), StaticFiles(config.FRONT_DIR))
    return ThreadingHTTPServer((host, port), handler)


def main():
    database = Database(config.DB_PATH)
    database.init()
    print(f"서버 실행 중: http://{config.HOST}:{config.PORT}  (종료: Ctrl+C)")
    create_server(database).serve_forever()


if __name__ == "__main__":
    main()
