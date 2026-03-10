from fastapi import Depends

from src.api.middlewares.access_token_middleware import get_current_auth_id
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.entities.user_entity import UserEntity
from src.domain.enums.user_role_enum import UserRoleEnum
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes
from src.domain.errors.unauthorized_error import UnauthorizedError
from src.repositories.user_repository import UserRepository


class HasPermissionUseCase:
    def __init__(self,role: UserRoleEnum, repository: UserRepository):
        self.__role = role
        self.__repository = repository

    def call(self, auth_id: int) -> CurrentUserEntity:
        user: CurrentUserEntity = self.__repository.find_current_user_by_auth_id(auth_id)

        if user.role_id != self.__role.value[0]:
            raise UnauthorizedError(code=UnauthorizedErrorCodes.INSUFFICIENT_PERMISSIONS.code())

        return user
