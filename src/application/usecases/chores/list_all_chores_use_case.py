from src.api.v1.requests.chores.get_chores_filtered_request import GetChoresFilteredRequest
from src.api.v1.responses.chores.chore_response import ChoreResponse
from src.api.v1.responses.chores.chores_paginated_response import (
    ChoresPaginatedResponse,
)
from src.domain.schemas.dto.chores.get_chores_filtered_dto import (
    GetChoresFilteredDto,
)
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class ListAllChoresUseCase:
    def __init__(self, chore_repository: ChoreRepository):
        self.chore_repository = chore_repository

    @logging(show_args=True, show_return=True)
    def execute(self, family_id: int, request: GetChoresFilteredRequest) -> ChoresPaginatedResponse:
        try:
            return self.__find_chores_paginated(family_id, request)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(
                code=InternalErrorCodes.LIST_CHORES_ERROR.code()
            )

    def __find_chores_paginated(self, family_id: int, request: GetChoresFilteredRequest) -> ChoresPaginatedResponse:
        dto = GetChoresFilteredDto(
            completed=request.completed,
            is_recurring=request.is_recurring,
            title=request.title,
            assigned_to_user_id=request.assigned_to_user_id,
            page_size=request.page_size,
            page=request.page,
        )
        result = self.chore_repository.find_paginated(
            family_id=family_id,
            dto=dto,
        )
        return ChoresPaginatedResponse(
            items=[ChoreResponse.from_entity(e) for e in result.items],
            total_items=result.total_items,
            page=result.page,
            page_size=result.page_size,
            total_pages=result.total_pages,
        )
