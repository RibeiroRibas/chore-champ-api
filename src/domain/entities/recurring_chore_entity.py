from src.domain.entities.day_of_week_entity import DayOfWeekEntity


class RecurringChoreEntity:
    def __init__(
        self,
        chore_id: int,
        day_of_week: DayOfWeekEntity,
        parent_chore_id: int | None = None,
    ):
        self.chore_id = chore_id
        self.day_of_week = day_of_week
        self.parent_chore_id = parent_chore_id
