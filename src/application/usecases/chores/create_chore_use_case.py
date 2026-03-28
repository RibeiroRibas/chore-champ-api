from src.api.v1.requests.chores.create_chore_request import CreateChoreRequest
from src.domain.schemas.dto.chores.create_chore_dto import CreateChoreDTO
from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.services.create_chore_service import CreateChoreService
from src.infra.decorators.logger import logging


class CreateChoreUseCase:
    def __init__(self, create_chore_service: CreateChoreService):
        self.__create_chore_service = create_chore_service

    @logging(show_args=True, show_return=True)
    def call(self, request: CreateChoreRequest, current_user: CurrentUserEntity) -> bool:
        try:
            return self.__create(request, current_user)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.CREATE_CHORE_ERROR.code())

    def __create(self, request: CreateChoreRequest, current_user: CurrentUserEntity) -> bool:
        if request.is_recurring and (
            request.recurrence_day_ids is None or len(request.recurrence_day_ids) == 0
        ):
            raise BadRequestError(code=BadRequestErrorCode.RECURRENCE_DAY_IDS_REQUIRED.code())

        if request.is_recurring and request.completed:
            raise BadRequestError(code=BadRequestErrorCode.CAN_NOT_CREATE_COMPLETED_RECURRING.code())

        assignee_ids = list(dict.fromkeys(request.assigned_to_user_ids))
        current_user.validate_chore_create_assignees(assignee_ids)

        reward_unlocked_response = False
        if len(assignee_ids) == 0:
            reward_unlocked_response = self.__create_chore(request, current_user)
        else:
            for uid in assignee_ids:
                should_commit = assignee_ids[len(assignee_ids) -1] == uid
                reward_unlocked = self.__create_chore(request, current_user, uid, should_commit)
                reward_unlocked_response = reward_unlocked_response or reward_unlocked

        return reward_unlocked_response

    def __create_chore(
        self,
        request: CreateChoreRequest,
        current_user: CurrentUserEntity,
        assigned_to_user_id: int | None = None,
        should_commit: bool = True,
    ) -> bool:
        dto = CreateChoreDTO(
            family_id=current_user.family_id,
            title=request.title,
            emoji=request.emoji,
            points=request.points,
            created_by_user_id=current_user.user_id,
            assigned_to_user_id=assigned_to_user_id,
            completed=request.completed,
            is_recurring=request.is_recurring,
            recurrence_day_ids=request.recurrence_day_ids,
        )
        return self.__create_chore_service.execute(dto, should_commit)
