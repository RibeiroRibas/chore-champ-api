from dataclasses import dataclass


@dataclass
class UpdateChoreDTO:
    title: str
    emoji: str
    points: int
    is_recurring: bool
    completed: bool
    assigned_to_user_id: int | None = None
    recurrence_day_ids: list[int] | None = None