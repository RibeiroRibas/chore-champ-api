import os

from src.api.v1.requests.auth.create_auth_request import CreateAuthRequest
from src.application.schemas.auth.create_auth_dto import CreateAuthDTO
from src.application.usecases.auth.validate_email_code_checking_use_case import ValidateEmailCodeCheckingUseCase
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
from src.domain.services.b_crypt_password_service import hash_password
from src.repositories.auth_repository import AuthRepository


class CreateAuthUseCase:
    def __init__(self, auth_repository: AuthRepository, validate_email_code_use_case: ValidateEmailCodeCheckingUseCase):
        self.validate_email_code_use_case = validate_email_code_use_case
        self.auth_repository = auth_repository
        self.is_email_code_checking_enabled = os.getenv('SEND_EMAIL_CODE_ENABLE') == "True"

    @logging(show_args=True, show_return=True)
    def execute(self, request: CreateAuthRequest):
        try:
            self.__create_auth(request)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.CREATE_AUTH_ERROR.code())

    def __create_auth(self, request: CreateAuthRequest):
        self.verify_email_in_use(str(request.email))
        self.__validate_email_code(request)
        self.__save_auth(request)

    def __validate_email_code(self, request: CreateAuthRequest):
        if self.is_email_code_checking_enabled:
            self.validate_email_code_use_case.execute(email=request.email, code=request.email_confirmation_code)

    def __save_auth(self, request: CreateAuthRequest):
        hashed_password = hash_password(request.password)
        auth_dto = CreateAuthDTO(username=request.email, password=hashed_password)
        self.auth_repository.insert(auth_dto=auth_dto)

    def verify_email_in_use(self, email: str):
        if self.auth_repository.exists_by_email(email=email):
            raise BadRequestError(code=BadRequestErrorCode.EMAIL_ALREADY_IN_USE.code())
