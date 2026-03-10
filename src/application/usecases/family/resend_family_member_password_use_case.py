import random
import string
from collections.abc import Callable

from src.domain.entities.user_auth_family_entity import UserAuthFamilyEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.services.b_crypt_password_service import hash_password
from src.domain.services.get_user_auth_family_service import GetUserAuthFamilyService
from src.infra.decorators.logger import logging
from src.repositories.auth_repository import AuthRepository


def _generate_temp_password(length: int = 12) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


class ResendFamilyMemberPasswordUseCase:
    def __init__(
        self,
        get_user_auth_family_service: GetUserAuthFamilyService,
        auth_repository: AuthRepository,
    ):
        self.get_user_auth_family_service = get_user_auth_family_service
        self.auth_repository = auth_repository

    @logging(show_args=True, show_return=False)
    def execute(
        self,
        user_id: int,
        family_id: int,
        send_email_async: Callable[[str, str]],
    ) -> None:
        try:
            self._resend_password(user_id, family_id, send_email_async)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.GET_CURRENT_USER_ERROR.code())

    def _resend_password(
        self,
        user_id: int,
        family_id: int,
        send_email_async: Callable[[str, str]],
    ) -> None:
        entity: UserAuthFamilyEntity = self.get_user_auth_family_service.execute(user_id, family_id)

        temp_password = _generate_temp_password()
        hashed = hash_password(temp_password)
        self.auth_repository.update_password(hashed, entity.auth.id)

        if send_email_async:
            send_email_async(entity.auth.username, temp_password)