from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.schemas.dto.chores.recurring_chore_dto import RecurringChoreDTO
from src.domain.schemas.entity.chore_user_entity import ChoreUserEntity
from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.domain.services.get_chore_user_service import GetChoreUSerService
from src.domain.services.recurring_chore_service import RecurringChoreService
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class DeleteChoreUseCase:
    def __init__(self, chore_repository: ChoreRepository, get_chore_user_service: GetChoreUSerService, recurring_chore_service: RecurringChoreService):
        self.__chore_repository = chore_repository
        self.__get_chore_user_service = get_chore_user_service
        self.__recurring_chore_service = recurring_chore_service


    @logging(show_args=True, show_return=False)
    def execute(self, chore_id: int, current_user: CurrentUserEntity) -> None:
        try:
            self.__process_delete_chore(chore_id, current_user)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.DELETE_CHORE_ERROR.code())

    def __process_delete_chore(self, chore_id: int, current_user: CurrentUserEntity):
        entity: ChoreUserEntity = self.__get_chore(chore_id, current_user)
        if entity.chore.is_recurring:
            self._deletee_recurring_chore(chore_id, current_user)
        self.__chore_repository.delete_by_id(chore_id, current_user.family_id)

    def _deletee_recurring_chore(self, chore_id: int, current_user: CurrentUserEntity):
        recurring_dto = RecurringChoreDTO(
            family_id=current_user.family_id,
            chore_id=chore_id,
            day_of_the_week_ids=[],
            is_recurring=True,
            is_chore_completed=False,
        )
        self.__recurring_chore_service.execute(dto=recurring_dto, commit=False)

    def __get_chore(self, chore_id: int, current_user: CurrentUserEntity)-> ChoreUserEntity:
        entity: ChoreUserEntity = self.__get_chore_user_service.execute(chore_id=chore_id,
                                                                        family_id=current_user.family_id)
        entity.chore.validate_has_delete_permission(current_user=current_user)
        entity.chore.validate_can_update_or_delete()
        return entity

