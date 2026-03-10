
from src.domain.entities.email_code_checking_entity import EmailCodeCheckingEntity
from src.infra.decorators.logger import logging
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.domain.errors.unauthorized_error import UnauthorizedError
from src.repositories.email_code_checking_repository import EmailCodeCheckingRepository


class ValidateEmailCodeCheckingUseCase:
    def __init__(self, email_code_checking_repository: EmailCodeCheckingRepository):
        self.email_code_checking_repository = email_code_checking_repository

    @logging(show_args=True, show_return=True)
    def execute(self, email: str, code: int) -> None:
        try:
            self.__validate_email_code(str(email), code)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(
                code=InternalErrorCodes.VALIDATE_EMAIL_CODE_INTERNAL_ERROR.code()
            )

    def __validate_email_code(self, email: str, code: int) -> None:
        email_code_checking: EmailCodeCheckingEntity | None = self.email_code_checking_repository.find_by_email(email)

        if not email_code_checking:
            raise NotFoundError(code=NotFoundErrorCodes.EMAIL_CODE_CHECKING_NOT_FOUND.code())

        email_code_checking.validate(code)

        if email_code_checking.validated:
            self.email_code_checking_repository.update(email_code_checking=email_code_checking)
            return

        self.__update_email_attempts_and_raise_error(email_code_checking)

    def __update_email_attempts_and_raise_error(self, email_code_checking: EmailCodeCheckingEntity) -> None:
        email_code_checking.update_attempts()
        self.email_code_checking_repository.update(email_code_checking=email_code_checking)

        raise UnauthorizedError(code=UnauthorizedErrorCodes.EMAIL_CODE_INVALID.code())
