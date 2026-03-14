from src.api.v1.responses.auth.login_response import LoginResponse
from src.domain.entities.refresh_token_entity import RefreshTokenEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.unauthorized_error import UnauthorizedError
from src.infra.decorators.logger import logging
from src.infra.services.jwt_service import JWTService
from src.domain.services.generate_refresh_token_service import GenerateRefreshTokenService
from src.repositories.refresh_token_repository import RefreshTokenRepository


class RefreshTokenUseCase:
    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepository,
        generate_refresh_token_service: GenerateRefreshTokenService,
        jwt_service: JWTService,
    ):
        self.refresh_token_repository = refresh_token_repository
        self.generate_refresh_token_service = generate_refresh_token_service
        self.jwt_service = jwt_service

    @logging(show_args=True, show_return=True)
    def execute(self, refresh_token: str, current_auth_id: int) -> LoginResponse:
        try:
            return self.__refresh(refresh_token=refresh_token, current_auth_id=current_auth_id)
        except Exception as e:
            if isinstance(e, BaseError):
                raise e
            raise InternalError(code=InternalErrorCodes.REFRESH_TOKEN_ERROR.code())

    def __refresh(self, refresh_token: str, current_auth_id: int) -> LoginResponse:
        entity: RefreshTokenEntity = self.__get_and_validate(current_auth_id, refresh_token)

        new_refresh_token = self.generate_refresh_token_service.execute(auth_id=current_auth_id)
        new_access_token = self.jwt_service.generate_token(auth_id=entity.auth_id)

        return LoginResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )

    def __get_and_validate(self, current_auth_id: int, refresh_token: str) -> RefreshTokenEntity:
        entity: RefreshTokenEntity | None = self.refresh_token_repository.find_by_refresh_token_and_auth_id(
            refresh_token=refresh_token, auth_id=current_auth_id)

        if not entity:
            raise UnauthorizedError(code=UnauthorizedErrorCodes.REFRESH_TOKEN_INVALID.code())

        return entity
