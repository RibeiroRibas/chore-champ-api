from src.api.v1.responses.auth.login_response import LoginResponse
from src.domain.entities.auth_entity import AuthEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes
from src.domain.errors.unauthorized_error import UnauthorizedError
from src.infra.decorators.logger import logging
from src.infra.services.jwt_service import JWTService
from src.repositories.auth_repository import AuthRepository


class LoginUseCase:
    def __init__(self, auth_repository: AuthRepository, jwt_service: JWTService):
        self.auth_repository = auth_repository
        self.jwt_service = jwt_service

    @logging(show_args=True, show_return=True)
    def execute(self, username: str, password) -> LoginResponse:
        try:
            return self.__login(username=username, password=password)
        except Exception as e:
            if isinstance(e, BaseError):
                raise e
            raise UnauthorizedError(code=InternalErrorCodes.LOGIN_INTERNAL_ERROR.code())

    def __login(self, username: str, password) -> LoginResponse:
        auth_entity: AuthEntity | None = self.auth_repository.find_by_username(username)

        if not auth_entity or not auth_entity.is_password_equals(plain_password=password):
            raise UnauthorizedError(code=UnauthorizedErrorCodes.INVALID_USER_CREDENTIALS.code())

        token = self.jwt_service.generate_token(auth_id=auth_entity.id)

        return LoginResponse(
            access_token=token,
            refresh_token=None
        )
