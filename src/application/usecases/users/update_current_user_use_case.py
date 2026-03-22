from src.api.v1.requests.users.update_current_user_request import UpdateCurrentUserRequest
from src.domain.schemas.dto.users.update_user_dto import UpdateUserDTO
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.vo.phone import PhoneVO
from src.infra.decorators.logger import logging
from src.repositories.user_repository import UserRepository


class UpdateCurrentUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @logging(show_args=True, show_return=True)
    def execute(self, request: UpdateCurrentUserRequest, auth_id: int):
        try:
            self.__update_user(request, auth_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.CREATE_AUTH_ERROR.code())

    def __update_user(self, request: UpdateCurrentUserRequest, auth_id: int):
        phone = PhoneVO.from_raw(request.phone)
        user_dto = UpdateUserDTO(name=request.name, phone=phone)
        self.user_repository.update(user_dto=user_dto, user_id=auth_id)
