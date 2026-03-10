from src.api.v1.requests.users.create_current_user_request import CreateCurrentUserRequest
from src.application.schemas.users.create_user_dto import CreateUserDTO
from src.domain.enums.user_role_enum import UserRoleEnum
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.vo.phone import PhoneVO
from src.infra.decorators.logger import logging
from src.repositories.family_repository import FamilyRepository
from src.repositories.user_repository import UserRepository


class CreateCurrentUserAndFamilyUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        family_repository: FamilyRepository,
    ):
        self.user_repository = user_repository
        self.family_repository = family_repository

    @logging(show_args=True, show_return=True)
    def execute(self, request: CreateCurrentUserRequest, auth_id: int):
        try:
            self.__create_family_and_user(request, auth_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.CREATE_CURRENT_USER_ERROR.code())

    def __create_family_and_user(self, request: CreateCurrentUserRequest, auth_id: int):
        self.__validate_user_exists(auth_id)
        family_id = self.family_repository.insert(name=request.family_name, commit=False)
        self.__create_user(auth_id=auth_id, request=request, family_id=family_id)

    def __create_user(self, auth_id: int, request: CreateCurrentUserRequest, family_id: int) -> int:
        phone = PhoneVO.from_raw(request.phone)
        user_dto = CreateUserDTO(
            name=request.name,
            auth_id=auth_id,
            role_id=UserRoleEnum.ADMIN.value[0],
            phone=phone,
            family_id=family_id,
        )
        return self.user_repository.insert(user_dto=user_dto)

    def __validate_user_exists(self, auth_id: int):
        exists_user: bool = self.user_repository.exists_by_auth_id(auth_id)

        if exists_user:
            raise BadRequestError(code=BadRequestErrorCode.USER_ALREADY_REGISTERED_FOR_THIS_AUTH.code())
