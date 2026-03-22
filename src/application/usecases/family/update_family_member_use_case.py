from src.api.v1.requests.users.update_family_member_request import UpdateFamilyMemberRequest
from src.api.v1.responses.users.family_member_response import FamilyMemberResponse
from src.domain.schemas.dto.users.update_user_dto import UpdateUserDTO
from src.domain.enums.user_role_enum import UserRoleEnum
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.services.get_role_by_id_service import GetRoleByIdService
from src.domain.services.get_user_family_service import GetUserFamilyService
from src.domain.services.validate_family_has_more_then_one_admin_service import ValidateFamilyMoreThenOneAdminService
from src.domain.vo.phone import PhoneVO
from src.infra.decorators.logger import logging
from src.repositories.auth_repository import AuthRepository
from src.repositories.user_repository import UserRepository


class UpdateFamilyMemberUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        get_role_by_id_service: GetRoleByIdService,
        get_user_family_service: GetUserFamilyService,
        auth_repository: AuthRepository,
        validate_family_has_more_then_one_admin_service: ValidateFamilyMoreThenOneAdminService
    ):
        self.user_repository = user_repository
        self.get_role_by_id_service = get_role_by_id_service
        self.get_user_family_service = get_user_family_service
        self.auth_repository = auth_repository
        self.validate_family_has_more_then_one_admin_service = validate_family_has_more_then_one_admin_service


    @logging(show_args=True, show_return=True)
    def execute(
        self,
        user_id: int,
        family_id: int,
        request: UpdateFamilyMemberRequest,
    ) -> FamilyMemberResponse:
        try:
            return self._update_member(user_id, family_id, request)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.UPDATE_FAMILY_MEMBER_ERROR.code())

    def _update_member(
        self,
        user_id: int,
        family_id: int,
        request: UpdateFamilyMemberRequest,
    ) -> FamilyMemberResponse:
        if UserRoleEnum.COLLABORATOR.value[0] == request.role_id:
            self.validate_family_has_more_then_one_admin_service.execute(family_id)

        entity = self.get_user_family_service.execute(user_id, family_id)

        phone = PhoneVO.from_raw(request.phone)
        self.__update_user(request, user_id, phone)
        self.auth_repository.update_username(entity.user.auth_id, request.email)

        role = self.get_role_by_id_service.execute(request.role_id)

        return FamilyMemberResponse(
            id=user_id,
            name=request.name,
            email=request.email,
            phone_number=phone.formatted(),
            role_id=role.id,
            role_name=role.name,
            avatar=request.avatar or entity.user.avatar or "👤",
        )

    def __update_user(self, request: UpdateFamilyMemberRequest, user_id: int, phone: PhoneVO):
        update_dto = UpdateUserDTO(name=request.name, phone=phone, avatar=request.avatar)
        self.user_repository.update(user_dto=update_dto, user_id=user_id, commit=False)