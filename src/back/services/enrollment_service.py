from ..errors import CohortFullError, NotFoundError
from ..models.enrollment import EnrollResult
from ..repositories import cohort_repo, enrollment_repo, student_repo


class EnrollmentService:
    def __init__(self, database):
        self.database = database

    def enroll(self, req):
        """수강 신청 업무 규칙. 한 트랜잭션이라 어느 단계에서든 실패하면 아무것도 남지 않는다.

        같은 이메일은 한 명의 수강생으로 보고, 같은 기수 중복과 정원 초과는 거절한다.
        """
        with self.database.transaction() as conn:
            cohort = cohort_repo.get(conn, req.cohort_id)
            if cohort is None:
                raise NotFoundError("존재하지 않는 기수입니다.")
            student = student_repo.get_by_email(conn, req.email) or student_repo.add(
                conn, req.name, req.phone, req.email, req.persona)
            if cohort.is_full(enrollment_repo.count_active(conn, cohort.id)):
                raise CohortFullError()
            enrollment = enrollment_repo.add(conn, student.id, cohort.id)
            return EnrollResult(student, cohort, enrollment)
