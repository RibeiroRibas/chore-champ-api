from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RecurringChoreDTO:
    family_id: int
    chore_id: int
    day_of_the_week_ids: list[int]
    is_chore_completed: bool
    is_recurring: bool

    def verify_day_match(self, day_of_week_id: int) -> bool:
        return self.day_of_the_week_ids.count(day_of_week_id) > 0

    def get_new_days_of_week(self, day_of_week_ids_from_db: list[int]) -> list[int]:
        return list(set(self.day_of_the_week_ids) - set(day_of_week_ids_from_db))

    def with_new_days(self, day_of_the_week_ids_to_add) -> RecurringChoreDTO:
        return RecurringChoreDTO(
            family_id=self.family_id,
            chore_id=self.chore_id,
            day_of_the_week_ids=day_of_the_week_ids_to_add,
            is_chore_completed=self.is_chore_completed,
            is_recurring=self.is_recurring,
        )

    def should_delete(self):
        return len(self.day_of_the_week_ids) == 0
