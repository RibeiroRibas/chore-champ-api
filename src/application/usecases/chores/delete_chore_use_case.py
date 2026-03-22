from src.domain.schemas.entity.chore_user_entity import ChoreUserEntity
from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.services.get_chore_user_service import GetChoreUSerService
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class DeleteChoreUseCase:
    def __init__(self, chore_repository: ChoreRepository, get_chore_user_service: GetChoreUSerService):
        self.__chore_repository = chore_repository
        self.__get_chore_user_service = get_chore_user_service


    @logging(show_args=True, show_return=False)
    def execute(self, chore_id: int, current_user: CurrentUserEntity) -> None:
        try:
            self.__process_delete_chore(chore_id, current_user)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.DELETE_CHORE_ERROR.code())

    def __process_delete_chore(self, chore_id: int, current_user: CurrentUserEntity):
        self.__validate_can_delete(chore_id, current_user)
        self.__chore_repository.delete_by_id(chore_id, current_user.family_id)

    def __validate_can_delete(self, chore_id: int, current_user: CurrentUserEntity):
        entity: ChoreUserEntity = self.__get_chore_user_service.execute(chore_id=chore_id, family_id=current_user.family_id)
        entity.chore.validate_has_delete_permission(current_user=current_user)
        entity.chore.validate_can_update_or_delete()
