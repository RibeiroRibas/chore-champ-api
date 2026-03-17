from dataclasses import dataclass


@dataclass
class RecurringChoreDTO:
    family_id: int
    chore_id: int
    is_chore_completed: bool = False
    is_recurring: bool | None = None
    day_of_the_week_ids: list[int] | None = None
    parent_chore_id: int | None = None
