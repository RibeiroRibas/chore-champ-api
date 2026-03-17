from dataclasses import dataclass


@dataclass
class CreateChoreDTO:
    family_id: int
    title: str
    emoji: str
    points: int
    created_by_user_id: int
    assigned_to_user_id: int | None = None
    completed: bool = False
    is_recurring: bool = False
    recurrence_day_ids: list[int] | None = None
