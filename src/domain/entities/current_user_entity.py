from src.domain.enums.user_role_enum import UserRoleEnum
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode


class CurrentUserEntity:
    def __init__(self, user_id: int, auth_id: int, role_id: int, family_id: int):
        self.user_id = user_id
        self.auth_id = auth_id
        self.role_id = role_id
        self.family_id = family_id

    def is_admin(self) -> bool:
        return self.role_id == UserRoleEnum.ADMIN.value[0]

    def validate_chore_create_assignees(self, assigned_to_user_ids: list[int]) -> None:
        if self.is_admin():
            return
        if len(assigned_to_user_ids) != 1 or assigned_to_user_ids[0] != self.user_id:
            raise BadRequestError(
                code=BadRequestErrorCode.COLLABORATOR_CREATE_CHORE_MUST_ASSIGN_TO_SELF.code()
            )
