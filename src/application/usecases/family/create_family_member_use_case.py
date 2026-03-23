from collections.abc import Callable

from src.api.v1.requests.users.create_family_member_request import CreateFamilyMemberRequest
from src.api.v1.responses.users.family_member_response import FamilyMemberResponse
from src.domain.schemas.dto.auth.create_auth_dto import CreateAuthDTO
from src.domain.schemas.dto.users.create_user_dto import CreateUserDTO
from src.domain.schemas.entity.role_entity import RoleEntity
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.services.get_role_by_id_service import GetRoleByIdService
from src.domain.services.password_service import hash_password, generate_temp_password
from src.domain.vo.phone import PhoneVO
from src.infra.decorators.logger import logging
from src.repositories.auth_repository import AuthRepository
from src.repositories.family_repository import FamilyRepository
from src.repositories.user_repository import UserRepository


class CreateFamilyMemberUseCase:
    def __init__(
            self,
            user_repository: UserRepository,
            family_repository: FamilyRepository,
            auth_repository: AuthRepository,
            get_role_by_id_service: GetRoleByIdService,
    ):
        self.user_repository = user_repository
        self.family_repository = family_repository
        self.auth_repository = auth_repository
        self.get_role_by_id_service = get_role_by_id_service

    @logging(show_args=True, show_return=True)
    def execute(
            self,
            request: CreateFamilyMemberRequest,
            family_id: int,
            send_email_async: Callable[[str, str], None]
    ) -> FamilyMemberResponse:
        try:
            return self._create_member(request, family_id, send_email_async)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.CREATE_FAMILY_MEMBER_ERROR.code())

    def _create_member(
            self,
            request: CreateFamilyMemberRequest,
            family_id: int,
            send_email_async: Callable[[str, str], None],
    ) -> FamilyMemberResponse:
        self.__validate_email_in_use(request)

        role: RoleEntity = self.get_role_by_id_service.execute(request.role_id)
        phone = PhoneVO.from_raw(request.phone)
        temp_password = generate_temp_password()
        hashed = hash_password(temp_password)

        auth_id = self.__create_auth(hashed, request)
        user_id = self.__create_user(auth_id, family_id, phone, request, role)

        send_email_async(request.email, temp_password)

        return FamilyMemberResponse(
            id=user_id,
            name=request.name,
            email=request.email,
            phone_number=phone.formatted(),
            role_id=role.id,
            role_name=role.name,
            avatar=request.avatar or "👤",
        )

    def __create_user(self, auth_id: int, family_id: int, phone: PhoneVO, request: CreateFamilyMemberRequest,
                      role: RoleEntity) -> int:
        user_dto = CreateUserDTO(
            name=request.name,
            auth_id=auth_id,
            role_id=role.id,
            phone=phone,
            family_id=family_id,
            avatar=request.avatar,
        )
        user_id = self.user_repository.insert(user_dto=user_dto)
        return user_id

    def __create_auth(self, hashed: str, request: CreateFamilyMemberRequest) -> int:
        auth_dto = CreateAuthDTO(username=request.email, password=hashed)
        auth_id = self.auth_repository.insert(auth_dto=auth_dto, commit=False)
        return auth_id

    def __validate_email_in_use(self, request: CreateFamilyMemberRequest):
        if self.auth_repository.exists_by_email(request.email):
            raise BadRequestError(code=BadRequestErrorCode.EMAIL_ALREADY_IN_USE.code())
