from src.application.usecases.auth.send_email_verification_code_use_case import SendEmailVerificationCodeUseCase
from src.infra.decorators.logger import logging
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.repositories.auth_repository import AuthRepository


class SendEmailCreateAuthCodeUseCase:
    def __init__(self, auth_repository: AuthRepository,
                 send_email_verification_code_use_case: SendEmailVerificationCodeUseCase):
        self.auth_repository = auth_repository
        self.send_email_verification_code_use_case = send_email_verification_code_use_case

    @logging(show_args=True, show_return=False)
    def execute(self, email: str):
        try:
            self.__prepare_and_send_email(email)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.SEND_EMAIL_CREATE_AUTH_CODE_ERROR.code())

    def __prepare_and_send_email(self, email: str):
        exists_by_email: bool = self.auth_repository.exists_by_email(email)

        if exists_by_email:
            raise BadRequestError(code=BadRequestErrorCode.EMAIL_ALREADY_IN_USE.code())

        self.send_email_verification_code_use_case.execute(email=email, subject="Confirmação de Criação de Conta")

