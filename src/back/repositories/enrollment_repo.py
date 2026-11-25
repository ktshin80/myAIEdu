import sqlite3

from ..errors import DuplicateEnrollmentError
from ..models.enrollment import Enrollment


def count_active(conn, cohort_id):
    """중도 포기(dropped)를 뺀 신청 인원."""
    return conn.execute(
        "SELECT COUNT(*) FROM enrollments WHERE cohort_id = ? AND status != 'dropped'",
        (cohort_id,)).fetchone()[0]


def add(conn, student_id, cohort_id):
    try:
        enrollment_id = conn.execute(
            "INSERT INTO enrollments (student_id, cohort_id) VALUES (?, ?)",
            (student_id, cohort_id)).lastrowid
    except sqlite3.IntegrityError:
        # (student_id, cohort_id) UNIQUE 위반: 저장소 세부사항을 업무 오류로 바꿔 올린다.
        raise DuplicateEnrollmentError() from None
    return Enrollment(enrollment_id, student_id, cohort_id, "enrolled")
