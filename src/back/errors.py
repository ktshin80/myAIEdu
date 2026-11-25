"""업무 오류. 상태 코드와 사용자 메시지를 담아 web 계층이 그대로 응답으로 바꾼다."""


class AppError(Exception):
    status = 500
    default_message = "서버 오류가 발생했습니다."

    def __init__(self, message=None):
        self.message = message or self.default_message
        super().__init__(self.message)


class ValidationError(AppError):
    status = 400
    default_message = "요청 형식이 올바르지 않습니다."


class NotFoundError(AppError):
    status = 404
    default_message = "찾을 수 없습니다."


class ConflictError(AppError):
    status = 409
    default_message = "요청이 현재 상태와 충돌합니다."


class DuplicateEnrollmentError(ConflictError):
    default_message = "이미 이 기수에 신청하셨습니다."


class CohortFullError(ConflictError):
    default_message = "정원이 마감된 기수입니다."
