from ..models.curriculum import TRACKS
from ..repositories import curriculum_repo


class CurriculumService:
    def __init__(self, database):
        self.database = database

    def list(self, track=""):
        # 알 수 없는 값은 오류 대신 전체 목록으로 본다(기존 동작 유지).
        track = track if track in TRACKS else None
        with self.database.session() as conn:
            return curriculum_repo.list_by_track(conn, track)
