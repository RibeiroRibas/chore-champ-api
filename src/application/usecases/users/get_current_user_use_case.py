from src.api.v1.responses.users.current_user_response import CurrentUserResponse
from src.domain.entities.user_entity import UserEntity
from src.domain.entities.user_family_entity import UserFamilyEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.infra.decorators.logger import logging
from src.repositories.user_repository import UserRepository


class GetCurrentUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @logging(show_args=True, show_return=True)
    def execute(self, auth_id: int) -> CurrentUserResponse:
        try:
            return self.__get_current_user(auth_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.GET_CURRENT_USER_ERROR.code())

    def __get_current_user(self, auth_id: int) -> CurrentUserResponse:
        user: UserFamilyEntity | None = self.user_repository.find_by_auth_id_with_family(auth_id)

        if user is None:
            raise NotFoundError(code=NotFoundErrorCodes.USER_NOT_FOUND.code())

        return CurrentUserResponse.from_entity(entity=user)