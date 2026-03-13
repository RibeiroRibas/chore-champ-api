import os

from src.application.usecases.auth.send_email_verification_code_use_case import SendEmailVerificationCodeUseCase
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.infra.decorators.logger import logging
from src.repositories.auth_repository import AuthRepository


class SendEmailForgetPasswordCodeUseCase:
    def __init__(self, auth_repository: AuthRepository,
                 send_email_verification_code_use_case: SendEmailVerificationCodeUseCase):
        self.auth_repository = auth_repository
        self.send_email_verification_code_use_case = send_email_verification_code_use_case
        self.is_email_code_disabled = os.getenv('SEND_EMAIL_CODE_ENABLE') == "False"

    @logging(show_args=True, show_return=False)
    def execute(self, email: str):
        try:
            self.__prepare_and_send_email(email)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.SEND_EMAIL_FORGET_PASSWORD_CODE_ERROR.code())

    def __prepare_and_send_email(self, email: str):
        exists_by_email: bool = self.auth_repository.exists_by_email(email)

        if not exists_by_email:
            raise NotFoundError(code=NotFoundErrorCodes.AUTH_NOT_FOUND.code())

        self.send_email_verification_code_use_case.execute(email=email, subject="Redefinição de Senha")

