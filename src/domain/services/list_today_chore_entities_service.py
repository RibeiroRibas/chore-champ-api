from datetime import datetime

from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.recurring_chore_entity import RecurringChoreEntity
from src.repositories.chore_repository import ChoreRepository
from src.repositories.recurring_chore_repository import RecurringChoreRepository


class ListTodayChoreEntitiesService:
    def __init__(
        self,
        chore_repository: ChoreRepository,
        recurring_chore_repository: RecurringChoreRepository,
    ):
        self.__chore_repository = chore_repository
        self.__recurring_chore_repository = recurring_chore_repository

    def execute(self, family_id: int) -> list[ChoreEntity]:
        chores = self.__chore_repository.find_today_chore_by_family_id(family_id)

        non_recurring = [e for e in chores if not e.is_recurring]
        recurring = [e for e in chores if e.is_recurring]

        filtered_recurring_for_today = self.__filter_recurring_chores_for_today(
            family_id, recurring
        )

        result = non_recurring + filtered_recurring_for_today
        return result

    def __filter_recurring_chores_for_today(
        self, family_id: int, recurring: list[ChoreEntity]
    ) -> list[ChoreEntity]:
        current_day_id = datetime.now().weekday() + 1
        all_recurring_for_today: list[RecurringChoreEntity] = (
            self.__recurring_chore_repository.find_by_parent_chore_id_and_day(
                family_id=family_id,
                day_of_week_id=current_day_id,
            )
        )

        filtered_recurring_for_today: list[ChoreEntity] = []
        for recurring_for_today in all_recurring_for_today:
            for recurring_chore in recurring:
                if recurring_chore.id == recurring_for_today.chore_id:
                    if not recurring_for_today.parent_chore_id:
                        filtered_recurring_for_today.append(recurring_chore)

                if recurring_chore.id == recurring_for_today.parent_chore_id:
                    chore = self.__chore_repository.find_by_id(
                        chore_id=recurring_for_today.chore_id,
                        family_id=family_id,
                    )
                    recurring_chore.recurrence_day_ids = chore.recurrence_day_ids
                    filtered_recurring_for_today.append(recurring_chore)

        return filtered_recurring_for_today
