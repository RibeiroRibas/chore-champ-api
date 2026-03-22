from src.api.v1.requests.auth.reset_password_request import ResetPasswordRequest
from src.application.usecases.auth.validate_email_code_checking_use_case import ValidateEmailCodeCheckingUseCase
from src.domain.schemas.entity.auth_entity import AuthEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.infra.decorators.logger import logging
from src.domain.services.password_service import hash_password
from src.repositories.auth_repository import AuthRepository


class ResetPasswordUseCase:
    def __init__(self, auth_repository: AuthRepository, validate_email_code_use_case: ValidateEmailCodeCheckingUseCase):
        self.auth_repository = auth_repository
        self.validate_email_code_use_case = validate_email_code_use_case

    @logging(show_args=True, show_return=True)
    def execute(self, request: ResetPasswordRequest):
        try:
            self.__reset_password(request)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.RESET_PASSWORD_ERROR.code())

    def __reset_password(self, request: ResetPasswordRequest):
        auth: AuthEntity = self.auth_repository.find_by_username(username=request.email)

        if not auth:
            raise NotFoundError(code=NotFoundErrorCodes.AUTH_NOT_FOUND.code())

        self.validate_email_code_use_case.execute(email=request.email, code=request.confirmation_code)

        hashed_password = hash_password(request.password)
        self.auth_repository.update_password(password=hashed_password, auth_id=auth.id)
