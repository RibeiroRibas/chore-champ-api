from dataclasses import dataclass

from src.domain.vo.phone import PhoneVO


@dataclass
class UpdateChoreDTO:
    title: str
    emoji: str
    points: int
    assigned_to_user_id: int | None = None
    completed: bool = False