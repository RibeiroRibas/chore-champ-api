from dataclasses import dataclass

from src.domain.vo.phone import PhoneVO


@dataclass
class CreateChoreDTO:
    family_id: int
    title: str
    emoji: str
    points: int
    created_by_user_id: int
    assigned_to_user_id: int | None = None
    completed: bool = False