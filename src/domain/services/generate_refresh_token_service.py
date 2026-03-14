import uuid

from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.repositories.refresh_token_repository import RefreshTokenRepository


class GenerateRefreshTokenService:
    def __init__(self, refresh_token_repository: RefreshTokenRepository):
        self.refresh_token_repository = refresh_token_repository

    def execute(self, auth_id: int) -> str:
        try:
            return self.__generate_refresh_token(auth_id)
        except Exception:
            raise InternalError(code=InternalErrorCodes.GENERATE_REFRESH_TOKEN_ERROR.code())

    def __generate_refresh_token(self, auth_id: int) -> str:
        self.refresh_token_repository.delete_by_auth_id(auth_id=auth_id, commit=False)
        token = str(uuid.uuid4())
        self.refresh_token_repository.insert(auth_id=auth_id, refresh_token=token)
        return token
