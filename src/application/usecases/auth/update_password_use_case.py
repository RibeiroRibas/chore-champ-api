from src.api.v1.requests.auth.update_password_request import UpdatePasswordRequest
from src.domain.entities.auth_entity import AuthEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.unauthorized_error import UnauthorizedError
from src.domain.services.password_service import hash_password
from src.infra.decorators.logger import logging
from src.repositories.auth_repository import AuthRepository


class UpdatePasswordUseCase:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    @logging(show_args=True, show_return=True)
    def execute(self, request: UpdatePasswordRequest, auth_id: int):
        try:
            self.__update_password(auth_id, request)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.UPDATE_PASSWORD_ERROR.code())

    def __update_password(self, auth_id: int, request: UpdatePasswordRequest):
        auth_entity: AuthEntity | None = self.auth_repository.find_by_id(auth_id)

        if not auth_entity or not auth_entity.is_password_equals(plain_password=request.old_password):
            raise UnauthorizedError(code=UnauthorizedErrorCodes.INVALID_USER_CREDENTIALS.code())

        hashed_password = hash_password(request.new_password)
        self.auth_repository.update_password(password=hashed_password, auth_id=auth_id)
