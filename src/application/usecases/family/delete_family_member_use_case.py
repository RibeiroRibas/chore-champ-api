from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.services.get_user_family_service import GetUserFamilyService
from src.infra.decorators.logger import logging
from src.repositories.auth_repository import AuthRepository
from src.repositories.user_repository import UserRepository


class DeleteFamilyMemberUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        auth_repository: AuthRepository,
        get_user_family_service: GetUserFamilyService,
    ):
        self.user_repository = user_repository
        self.auth_repository = auth_repository
        self.get_user_family_service = get_user_family_service

    @logging(show_args=True, show_return=False)
    def execute(self, user_id: int, family_id: int) -> None:
        try:
            self._delete_member(user_id, family_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.DELETE_FAMILY_MEMBER_ERROR.code())

    def _delete_member(self, user_id: int, family_id: int) -> None:
        user_family_entity = self.get_user_family_service.execute(user_id, family_id)

        auth_id = user_family_entity.user.auth_id
        self.user_repository.delete_by_id(user_id=user_id, commit=False)
        self.auth_repository.delete_by_id(auth_id)