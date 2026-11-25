from dataclasses import dataclass

PERSONAS = ("worker", "owner")


@dataclass(frozen=True)
class Student:
    id: int
    name: str
    phone: str | None
    email: str
    persona: str | None
    created_at: str
