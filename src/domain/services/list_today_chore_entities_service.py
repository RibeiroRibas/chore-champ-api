from datetime import datetime

from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.schemas.entity.chore_entity import ChoreEntity
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
        current_week_day = datetime.now().weekday() + 1
        chores = self.__chore_repository.find_today_chores(family_id, current_week_day)
        return chores
