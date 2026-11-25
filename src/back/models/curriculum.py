from dataclasses import dataclass

TRACKS = ("worker", "owner")  # 'common'은 모든 트랙에 항상 포함된다.


@dataclass(frozen=True)
class CurriculumItem:
    id: int
    week_start: int
    week_end: int
    title: str
    track: str
    deliverable: str | None
