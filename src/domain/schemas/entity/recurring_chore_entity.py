from datetime import datetime

from src.domain.schemas.entity.day_of_week_entity import DayOfWeekEntity


class RecurringChoreEntity:
    def __init__(
        self,
        chore_id: int,
        day_of_week: DayOfWeekEntity,
        completed_at: datetime | None = None,
    ):
        self.chore_id = chore_id
        self.day_of_week = day_of_week
        self.completed_at = completed_at