from src.api.v1.responses.users.family_member_response import FamilyMemberResponse
from src.domain.schemas.entity.family_entity import FamilyEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
from src.repositories.family_repository import FamilyRepository


class ListFamilyMembersUseCase:
    def __init__(self, family_repository: FamilyRepository):
        self.family_repository = family_repository

    @logging(show_args=True, show_return=True)
    def execute(self, family_id: int) -> list[FamilyMemberResponse]:
        try:
            return self._list_members(family_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.LIST_FAMILY_MEMBERS_ERROR.code())

    def _list_members(self, family_id: int) -> list[FamilyMemberResponse]:
        family: FamilyEntity = self.family_repository.find_by_id_with_members(family_id)
        if family is None:
            return []
        return [
            FamilyMemberResponse.from_user_entity(member)
            for member in family.members
        ]
