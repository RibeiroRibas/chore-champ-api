import os
import random

from src.domain.schemas.dto.create_email_code_checking_dto import CreateEmailCodeCheckingDTO
from src.infra.decorators.logger import logging
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.services import send_email_service
from src.repositories.email_code_checking_repository import EmailCodeCheckingRepository


class SendEmailVerificationCodeUseCase:
    def __init__(self, email_code_checking_repository: EmailCodeCheckingRepository):
        self.email_code_checking_repository = email_code_checking_repository
        self.code_expiration_minutes: int = 15
        self.is_email_code_disabled = os.getenv('SEND_EMAIL_CODE_ENABLE') == "False"

    @logging(show_args=True, show_return=False)
    def execute(self, email: str, subject: str):
        try:
            self.__prepare_and_send_email(email, subject)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.SEND_EMAIL_VERIFICATION_CODE_ERROR.code())

    def __prepare_and_send_email(self, email: str, subject: str):
        if self.is_email_code_disabled:
            raise BadRequestError(code=BadRequestErrorCode.SEND_EMAIL_CODE_DISABLED.code())

        four_digit_code_generated = ''.join(str(random.randint(0, 9)) for _ in range(4))

        self.__send_email(email, four_digit_code_generated, subject)

        self.__create_email_code_checking(email, four_digit_code_generated)

    def __send_email(self, email: str, four_digit_code_generated: str, subject: str):
        rendered_template: str = self.__render_template(code=four_digit_code_generated)
        send_email_service.send(template_str=rendered_template, email=email, subject=subject)

    def __create_email_code_checking(self, email: str, four_digit_code_generated: str):
        email_code_checking = CreateEmailCodeCheckingDTO(email=email, code=int(four_digit_code_generated))
        self.email_code_checking_repository.delete_and_insert(email_code_checking)

    def __render_template(self, code: str) -> str:
        message_variables: dict = {
            "expiry_minutes": self.code_expiration_minutes,
            "code": code,
        }

        return send_email_service.render_template(message_variables=message_variables, template_name="send_email_verification_code_template.html")
