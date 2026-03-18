from src.api.v1.responses.chores.chore_response import ChoreResponse
from src.application.schemas.chores.update_chore_dto import UpdateChoreDTO
from src.application.schemas.users.add_user_points_dto import AddUserPointsDTO
from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.schemas.recurring_chore_dto import RecurringChoreDTO
from src.domain.services.get_chore_service import GetChoreService
from src.domain.services.recurring_chore_service import RecurringChoreService
from src.domain.services.save_user_points_service import SaveUserPointsService
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class CompleteChoreUseCase:
    def __init__(
        self,
        chore_repository: ChoreRepository,
        get_chore_service: GetChoreService,
        recurring_chore_service: RecurringChoreService,
        save_user_points_service: SaveUserPointsService,
    ):
        self.chore_repository = chore_repository
        self.get_chore_service = get_chore_service
        self.recurring_chore_service = recurring_chore_service
        self.save_user_points_service = save_user_points_service

    @logging(show_args=True, show_return=True)
    def execute(self, chore_id: int, current_user: CurrentUserEntity) -> ChoreResponse:
        try:
            return self.__complete_chore(chore_id=chore_id, current_user=current_user)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.COMPLETE_CHORE_ERROR.code())

    def __complete_chore(self, chore_id: int, current_user: CurrentUserEntity) -> ChoreResponse:
        chore = self.__get_chore_by_id(chore_id, current_user)
        chore.validate_can_complete(current_user=current_user)
        self.__save_user_points(chore, current_user)

        if chore.is_recurring:
            self.__handle_recurring_chore(chore_id, current_user, chore)

        updated: ChoreEntity = self.__update_chore(chore, current_user)

        return ChoreResponse.from_entity(updated)

    def __get_chore_by_id(self, chore_id: int, current_user: CurrentUserEntity) -> ChoreEntity:
        chore: ChoreEntity = self.get_chore_service.execute(
            chore_id=chore_id,
            family_id=current_user.family_id,
        )

        return chore

    def __save_user_points(self, chore: ChoreEntity, current_user: CurrentUserEntity):
        points_dto = AddUserPointsDTO(
            user_id=chore.assigned_to_user_id,
            points=chore.points,
            family_id=current_user.family_id,
        )
        self.save_user_points_service.execute(dto=points_dto)

    def __handle_recurring_chore(self, chore_id: int, current_user: CurrentUserEntity, updated: ChoreEntity):
        recurring_dto = RecurringChoreDTO(
            family_id=current_user.family_id,
            chore_id=chore_id,
            day_of_the_week_ids=updated.recurrence_day_ids,
            is_recurring=updated.is_recurring,
            is_chore_completed=True,
        )
        self.recurring_chore_service.execute(recurring_dto)

    def __update_chore(self, chore: ChoreEntity, current_user: CurrentUserEntity) -> ChoreEntity:
        dto = UpdateChoreDTO(
            title=chore.title,
            emoji=chore.emoji,
            points=chore.points,
            assigned_to_user_id=chore.assigned_to_user_id,
            completed=True,
            is_recurring=chore.is_recurring,
        )

        updated: ChoreEntity = self.chore_repository.update(
            chore_id=chore.id,
            family_id=current_user.family_id,
            update_chore_dto=dto,
        )
        return updated
