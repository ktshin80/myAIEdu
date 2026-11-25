import re
from dataclasses import dataclass

from ..errors import ValidationError
from .cohort import Cohort
from .student import PERSONAS, Student

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class Enrollment:
    id: int
    student_id: int
    cohort_id: int
    status: str


@dataclass(frozen=True)
class EnrollRequest:
    """수강 신청 입력. 형식 검증은 여기서 끝내고, 서비스는 업무 규칙만 다룬다."""
    name: str
    email: str
    phone: str
    persona: str | None
    cohort_id: int

    @classmethod
    def from_payload(cls, data):
        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip().lower()
        phone = str(data.get("phone", "")).strip()
        persona = data.get("persona") or None
        cohort_id = data.get("cohort_id")
        if not name or not EMAIL_RE.match(email):
            raise ValidationError("이름과 올바른 이메일을 입력해 주세요.")
        if persona not in (None, *PERSONAS):
            raise ValidationError("유형 값이 올바르지 않습니다.")
        if not isinstance(cohort_id, int) or isinstance(cohort_id, bool):
            raise ValidationError("기수를 선택해 주세요.")
        return cls(name, email, phone, persona, cohort_id)


@dataclass(frozen=True)
class EnrollResult:
    student: Student
    cohort: Cohort
    enrollment: Enrollment
