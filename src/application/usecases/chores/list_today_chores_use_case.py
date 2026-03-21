from src.api.v1.responses.chores.chore_response import ChoreResponse
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.services.list_today_chore_entities_service import (
    ListTodayChoreEntitiesService,
)
from src.infra.decorators.logger import logging


class ListTodayChoresUseCase:
    def __init__(self, list_today_chore_entities_service: ListTodayChoreEntitiesService):
        self.__list_today_chore_entities_service = list_today_chore_entities_service

    @logging(show_args=True, show_return=True)
    def execute(self, family_id: int) -> list[ChoreResponse]:
        try:
            return self.__list_today_chores(family_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.LIST_CHORES_ERROR.code())

    def __list_today_chores(self, family_id: int) -> list[ChoreResponse]:
        result = self.__list_today_chore_entities_service.execute(family_id)
        return [ChoreResponse.from_entity(e) for e in result]
