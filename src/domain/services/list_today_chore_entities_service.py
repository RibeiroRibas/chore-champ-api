from datetime import datetime

from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.recurring_chore_entity import RecurringChoreEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
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

    @logging(show_args=True, show_return=True)
    def execute(self, family_id: int) -> list[ChoreEntity]:
        try:
            return self.__list_today(family_id=family_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.LIST_TODAY_CHORE_ENTITIES_SERVICE_ERROR.code())

    def __list_today(self, family_id: int) -> list[ChoreEntity]:
        chores = self.__chore_repository.find_today_chore_by_family_id(family_id)

        non_recurring = [e for e in chores if not e.is_recurring]
        recurring = [e for e in chores if e.is_recurring]

        filtered_recurring_for_today = self.__filter_recurring_chores_for_today(
            family_id, recurring
        )

        return non_recurring + filtered_recurring_for_today

    def __filter_recurring_chores_for_today(
        self, family_id: int, recurring: list[ChoreEntity]
    ) -> list[ChoreEntity]:
        all_recurring_for_today = self.__get_all_recurring_for_today(family_id)

        return self.__filter_recurring_for_today(all_recurring_for_today, family_id, recurring)

    def __filter_recurring_for_today(self, all_recurring_for_today: list[RecurringChoreEntity], family_id: int,
                                     recurring: list[ChoreEntity]) -> list[ChoreEntity]:
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

    def __get_all_recurring_for_today(self, family_id: int) -> list[RecurringChoreEntity]:
        current_day_id = datetime.now().weekday() + 1
        all_recurring_for_today: list[RecurringChoreEntity] = (
            self.__recurring_chore_repository.find_by_parent_chore_id_and_day(
                family_id=family_id,
                day_of_week_id=current_day_id,
            )
        )
        return all_recurring_for_today
