from __future__ import annotations

from datetime import datetime

from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.domain.schemas.entity.day_of_week_entity import DayOfWeekEntity
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes
from src.domain.errors.unauthorized_error import UnauthorizedError


class ChoreEntity:
    def __init__(
        self,
        chore_id: int,
        family_id: int,
        title: str,
        emoji: str,
        points: int,
        assigned_to_user_id: int | None,
        created_by_user_id: int,
        completed: bool,
        is_recurring: bool = False,
        recurrence_days: list[DayOfWeekEntity] | None = None,
    ):
        self.id = chore_id
        self.family_id = family_id
        self.title = title
        self.emoji = emoji
        self.points = points
        self.assigned_to_user_id = assigned_to_user_id
        self.created_by_user_id = created_by_user_id
        self.completed = completed
        self.is_recurring = is_recurring
        self.recurrence_days = recurrence_days or []


    def validate_can_update_or_delete(self):
        if self.completed:
           raise BadRequestError(code=BadRequestErrorCode.CANNOT_UPDATE_OR_DELETE_CHORE_AFTER_COMPLETED.code())

    def validate_has_update_permission(self, current_user: CurrentUserEntity):
        if  current_user.is_admin() or self.created_by_user_id == current_user.user_id:
            return

        raise UnauthorizedError(code=UnauthorizedErrorCodes.CURRENT_USER_CANNOT_UPDATE_CHORE.code())

    def validate_has_delete_permission(self, current_user: CurrentUserEntity):
        if current_user.is_admin() or self.created_by_user_id == current_user.user_id:
            return

        raise UnauthorizedError(code=UnauthorizedErrorCodes.CURRENT_USER_CANNOT_DELETE_CHORE.code())

    def validate_can_assign_to_current_user(self, current_user: CurrentUserEntity):
        if self.completed:
            raise BadRequestError(code=BadRequestErrorCode.CHORE_ALREADY_COMPLETED.code())

        if not current_user.is_admin() and self.assigned_to_user_id is not None:
            raise BadRequestError(code=BadRequestErrorCode.CHORE_ALREADY_ASSIGNED.code())

    def validate_can_remove_assignment(self, current_user: CurrentUserEntity):
        if self.completed:
            raise BadRequestError(code=BadRequestErrorCode.CHORE_ALREADY_COMPLETED.code())

        if self.assigned_to_user_id is None:
            raise BadRequestError(code=BadRequestErrorCode.CHORE_CANNOT_REMOVE_ASSIGNMENT.code())

        if not current_user.is_admin():
            raise BadRequestError(
                code=BadRequestErrorCode.ONLY_ADMIN_CAN_REMOVE_CHORE_ASSIGNMENT.code()
            )

    def validate_can_complete(
        self, current_user: CurrentUserEntity, today_chores: list[ChoreEntity]
    ) -> None:
        if self.completed:
            raise BadRequestError(code=BadRequestErrorCode.CHORE_ALREADY_COMPLETED.code())

        if not current_user.is_admin():
            if self.assigned_to_user_id is None or self.assigned_to_user_id != current_user.user_id:
                raise BadRequestError(code=BadRequestErrorCode.CHORE_CANNOT_COMPLETE.code())

            if not self.is_chore_in_today_list(today_chores):
                raise BadRequestError(
                    code=BadRequestErrorCode.COLLABORATOR_CAN_ONLY_COMPLETE_TODAY_CHORES.code()
                )

        current_week_day: int = datetime.today().weekday() + 1
        recurrency_day_id: list[int] = [recurrence_day.id for recurrence_day in self.recurrence_days]
        if recurrency_day_id and current_week_day not in recurrency_day_id:
            raise BadRequestError(code=BadRequestErrorCode.CHORE_CAN_ONLY_BE_COMPLETED_TODAY.code())

    def is_chore_in_today_list(self, today_chores: list[ChoreEntity]) -> bool:
        return any(e.id == self.id for e in today_chores)

