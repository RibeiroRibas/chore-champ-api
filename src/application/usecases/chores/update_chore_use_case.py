from src.api.v1.requests.chores.update_chore_request import UpdateChoreRequest
from src.application.schemas.chores.update_chore_dto import UpdateChoreDTO
from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.schemas.recurring_chore_dto import RecurringChoreDTO
from src.domain.services.get_chore_service import GetChoreService
from src.domain.services.recurring_chore_service import RecurringChoreService
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class UpdateChoreUseCase:
    def __init__(self, chore_repository: ChoreRepository, get_chore_service: GetChoreService,
                 recurring_chore_service: RecurringChoreService):
        self.chore_repository = chore_repository
        self.get_chore_service = get_chore_service
        self.recurring_chore_service = recurring_chore_service

    @logging(show_args=True, show_return=True)
    def execute(self, chore_id: int, current_user: CurrentUserEntity, request: UpdateChoreRequest):
        try:
            self.__process_update_chore(chore_id, current_user, request)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.UPDATE_CHORE_ERROR.code())

    def __process_update_chore(self, chore_id: int, current_user: CurrentUserEntity, request: UpdateChoreRequest):
        if request.is_recurring and (request.recurrence_day_ids is None or len(request.recurrence_day_ids) == 0):
            raise BadRequestError(code=BadRequestErrorCode.RECURRENCE_DAY_IDS_REQUIRED.code())

        self.__validate_can_update(chore_id, current_user)
        updated = self.__update_chore(chore_id, current_user, request)
        if request.is_recurring:
            self.update_recurring_chore(current_user, updated, request)

    def __update_chore(self, chore_id: int, current_user: CurrentUserEntity,
                       request: UpdateChoreRequest) -> ChoreEntity:
        should_commit = request.is_recurring is False
        dto = UpdateChoreDTO(
            title=request.title,
            emoji=request.emoji,
            points=request.points,
            assigned_to_user_id=request.assigned_to_user_id,
            completed=request.completed,
            is_recurring=request.is_recurring,
            recurrence_day_ids=request.recurrence_day_ids,
        )

        updated = self.chore_repository.update(
            chore_id=chore_id,
            family_id=current_user.family_id,
            update_chore_dto=dto,
            commit=should_commit
        )
        return updated

    def __validate_can_update(self, chore_id: int, current_user: CurrentUserEntity):
        entity: ChoreEntity = self.get_chore_service.execute(chore_id=chore_id, family_id=current_user.family_id)

        entity.validate_has_update_permission(current_user=current_user)
        entity.validate_can_update_or_delete()

    def update_recurring_chore(self, current_user: CurrentUserEntity, entity: ChoreEntity, request: UpdateChoreRequest):
        recurring_dto = RecurringChoreDTO(
            family_id=current_user.family_id,
            chore_id=entity.id,
            day_of_the_week_ids=request.recurrence_day_ids,
            is_recurring=request.is_recurring,
            is_chore_completed=request.completed,
        )
        self.recurring_chore_service.execute(recurring_dto)
