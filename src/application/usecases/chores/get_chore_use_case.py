from src.api.v1.responses.chores.chore_response import ChoreResponse
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class GetChoreUseCase:
    def __init__(self, chore_repository: ChoreRepository):
        self.chore_repository = chore_repository

    @logging(show_args=True, show_return=True)
    def execute(self, chore_id: int, family_id: int) -> ChoreResponse:
        try:
            return self.__get_by_id(chore_id, family_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.GET_CHORE_ERROR.code())

    def __get_by_id(self, chore_id: int, family_id: int) -> ChoreResponse:
        entity = self.chore_repository.find_by_id(chore_id, family_id)

        if entity is None:
            raise NotFoundError(code=NotFoundErrorCodes.CHORE_NOT_FOUND.code())

        return ChoreResponse.from_entity(entity)