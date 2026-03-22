from src.api.v1.responses.users.family_member_response import FamilyMemberResponse
from src.domain.schemas.entity.user_auth_family_entity import UserAuthFamilyEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.services.get_user_auth_family_service import GetUserAuthFamilyService
from src.infra.decorators.logger import logging
from src.repositories.user_repository import UserRepository


class GetFamilyMemberUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        get_user_auth_family_service: GetUserAuthFamilyService,
    ):
        self.user_repository = user_repository
        self.get_user_auth_family_service = get_user_auth_family_service

    @logging(show_args=True, show_return=True)
    def execute(self, user_id: int, family_id: int) -> FamilyMemberResponse:
        try:
            return self._get_member(user_id, family_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.GET_FAMILY_MEMBER_ERROR.code())

    def _get_member(self, user_id: int, family_id: int) -> FamilyMemberResponse:
        entity: UserAuthFamilyEntity = self.get_user_auth_family_service.execute(user_id, family_id)

        return FamilyMemberResponse(
            id=entity.user.id,
            name=entity.user.name,
            email=entity.auth.username,
            phone_number=entity.user.phone.formatted(),
            role_id=entity.user.role.id,
            role_name=entity.user.role.name,
            avatar=entity.user.avatar or "👤",
        )
