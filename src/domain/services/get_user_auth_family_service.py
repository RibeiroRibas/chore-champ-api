from src.domain.entities.user_auth_family_entity import UserAuthFamilyEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.infra.decorators.logger import logging
from src.repositories.user_repository import UserRepository


class GetUserAuthFamilyService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @logging(show_args=True, show_return=True)
    def execute(self, user_id: int, family_id: int) -> UserAuthFamilyEntity:
        try:
            return self.__user_family(user_id, family_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.GET_USER_FAMILY_ERROR.code())

    def __user_family(self, user_id: int, family_id: int) -> UserAuthFamilyEntity:
        user_family_auth_entity = self.user_repository.find_by_id_with_auth_and_family(user_id)

        if user_family_auth_entity is None or user_family_auth_entity.family.id != family_id:
            raise NotFoundError(code=NotFoundErrorCodes.USER_NOT_FOUND.code())

        return user_family_auth_entity