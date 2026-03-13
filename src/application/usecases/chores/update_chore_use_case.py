from src.api.v1.requests.chores.update_chore_request import UpdateChoreRequest
from src.api.v1.responses.chores.chore_response import ChoreResponse
from src.application.schemas.chores.update_chore_dto import UpdateChoreDTO
from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.chore_user_entity import ChoreUserEntity
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.services.get_chore_user_service import GetChoreUSerService
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class UpdateChoreUseCase:
    def __init__(self, chore_repository: ChoreRepository, get_chore_user_service: GetChoreUSerService):
        self.chore_repository = chore_repository
        self.get_chore_user_service = get_chore_user_service

    @logging(show_args=True, show_return=True)
    def execute(self, chore_id: int, current_user: CurrentUserEntity, request: UpdateChoreRequest) -> ChoreResponse:
        try:
            return self.__process_update_chore(chore_id, current_user, request)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.UPDATE_CHORE_ERROR.code())

    def __process_update_chore(self, chore_id: int, current_user: CurrentUserEntity, request: UpdateChoreRequest) -> ChoreResponse:
        self.__validate_can_update(chore_id, current_user)
        updated = self.__update_chore(chore_id, current_user, request)
        return ChoreResponse.from_entity(updated)

    def __update_chore(self, chore_id: int, current_user: CurrentUserEntity, request: UpdateChoreRequest) -> ChoreEntity:
        dto = UpdateChoreDTO(
            title=request.title,
            emoji=request.emoji,
            points=request.points,
            assigned_to_user_id=request.assigned_to_user_id,
            completed=request.completed
        )

        updated = self.chore_repository.update(
            chore_id=chore_id,
            family_id=current_user.family_id,
            update_chore_dto=dto
        )
        return updated

    def __validate_can_update(self, chore_id: int, current_user: CurrentUserEntity):
        entity: ChoreUserEntity = self.get_chore_user_service.execute(chore_id=chore_id,
                                                                      family_id=current_user.family_id)

        entity.validate_has_update_permission(current_user_id=current_user.user_id)
        entity.chore.validate_can_update_or_delete()
