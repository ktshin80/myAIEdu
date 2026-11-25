from dataclasses import dataclass


@dataclass(frozen=True)
class Cohort:
    id: int
    name: str
    start_date: str | None
    capacity: int | None  # None이면 정원 제한 없음

    def is_full(self, enrolled_count):
        return self.capacity is not None and enrolled_count >= self.capacity
