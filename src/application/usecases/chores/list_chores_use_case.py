from src.api.v1.responses.chores.chore_response import ChoreResponse
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class ListChoresUseCase:
    def __init__(self, chore_repository: ChoreRepository):
        self.chore_repository = chore_repository

    @logging(show_args=True, show_return=True)
    def execute(self, family_id: int) -> list[ChoreResponse]:
        try:
            entities = self.chore_repository.find_by_family_id(family_id)
            return [ChoreResponse.from_entity(e) for e in entities]
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.LIST_CHORES_ERROR.code())
