from src.api.v1.requests.chores.create_chore_request import CreateChoreRequest
from src.api.v1.responses.chores.chore_response import ChoreResponse
from src.application.schemas.chores.create_chore_dto import CreateChoreDTO
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.services.get_user_family_service import GetUserFamilyService
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class CreateChoreUseCase:
    def __init__(
        self,
        chore_repository: ChoreRepository,
        get_user_family_service: GetUserFamilyService,
    ):
        self.chore_repository = chore_repository
        self.get_user_family_service = get_user_family_service

    @logging(show_args=True, show_return=True)
    def execute(self, request: CreateChoreRequest, current_user: CurrentUserEntity) -> ChoreResponse:
        try:
            return self.__create_chore(request, current_user)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.CREATE_CHORE_ERROR.code())

    def __create_chore(self, request: CreateChoreRequest, current_user: CurrentUserEntity) -> ChoreResponse:
        dto = CreateChoreDTO(
            family_id=current_user.family_id,
            title=request.title,
            emoji=request.emoji,
            points=request.points,
            created_by_user_id=current_user.user_id,
            assigned_to_user_id=request.assigned_to_user_id,
            completed=request.completed,
        )

        entity = self.chore_repository.insert(create_chore_dto=dto)
        return ChoreResponse.from_entity(entity)
