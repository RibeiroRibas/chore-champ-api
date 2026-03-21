from src.application.schemas.chores.update_chore_dto import UpdateChoreDTO
from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.services.get_chore_service import GetChoreService
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class RemoveAssignChoreToMeUseCase:
    def __init__(self, chore_repository: ChoreRepository, get_chore_service: GetChoreService):
        self.chore_repository = chore_repository
        self.get_chore_service = get_chore_service

    @logging(show_args=True, show_return=True)
    def execute(self, chore_id: int, current_user: CurrentUserEntity) -> None:
        try:
            self.__remove_assign_chore_to_me(chore_id=chore_id, current_user=current_user)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.REMOVE_ASSIGN_CHORE_TO_ME_ERROR.code())

    def __remove_assign_chore_to_me(self, chore_id: int, current_user: CurrentUserEntity) -> None:
        chore: ChoreEntity = self.get_chore_service.execute(
            chore_id=chore_id,
            family_id=current_user.family_id,
        )

        chore.validate_can_remove_assignment(current_user=current_user)

        dto = UpdateChoreDTO(
            title=chore.title,
            emoji=chore.emoji,
            points=chore.points,
            assigned_to_user_id=None,
            completed=chore.completed,
            is_recurring=chore.is_recurring
        )
        self.chore_repository.update(
            chore_id=chore_id,
            family_id=current_user.family_id,
            update_chore_dto=dto,
        )
