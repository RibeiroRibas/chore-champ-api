from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.user_entity import UserEntity
from src.domain.enums.user_role_enum import UserRoleEnum
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes
from src.domain.errors.unauthorized_error import UnauthorizedError


class ChoreUserEntity:
    def __init__(self, user_entity: UserEntity | None, chore: ChoreEntity):
        self.user = user_entity
        self.chore = chore

    def validate_has_update_permission(self, current_user_id: int):
        if self.user is None or self.user.id == current_user_id or self.user.role.id == UserRoleEnum.ADMIN:
            return

        raise UnauthorizedError(code=UnauthorizedErrorCodes.CURRENT_USER_CANNOT_UPDATE_CHORE.code())

    def validate_has_delete_permission(self, current_user_id: int):
        if self.chore.created_by_user_id == current_user_id or self.user.role.id == UserRoleEnum.ADMIN:
            return

        raise UnauthorizedError(code=UnauthorizedErrorCodes.CURRENT_USER_CANNOT_UPDATE_CHORE.code())