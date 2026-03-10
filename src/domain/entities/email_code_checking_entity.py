from datetime import datetime, timedelta

from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes
from src.domain.errors.unauthorized_error import UnauthorizedError


class EmailCodeCheckingEntity:
    def __init__(self, id: int, email: str, code: int, is_blocked: bool, validated: bool, validation_attempts: int, created_at: datetime) -> None:
        self.id = id
        self.email = email
        self.code = code
        self.is_blocked = is_blocked
        self.validated = validated
        self.validation_attempts = validation_attempts
        self.created_at = created_at
        self.__max_sms_validation_attempts = 3
        self.__email_code_expiration_minutes = 15

    def validate(self, code: int):
        if self.validated:
            raise UnauthorizedError(code=UnauthorizedErrorCodes.EMAIL_CODE_VALIDATED.code())

        if self.__is_expired():
            raise UnauthorizedError(code=UnauthorizedErrorCodes.EMAIL_CODE_EXPIRED.code())

        if self.is_blocked:
            raise UnauthorizedError(code=UnauthorizedErrorCodes.EMAIL_CODE_BLOCKED.code())

        if self.code == code:
            self.validated = True

    def __is_expired(self) -> bool:
        return self.created_at + timedelta(minutes=int(self.__email_code_expiration_minutes)) < datetime.now()

    def update_attempts(self):
        self.validation_attempts += 1

        if self.validation_attempts == self.__max_sms_validation_attempts:
            self.is_blocked = True