from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
from src.repositories.family_repository import FamilyRepository


class ValidateFamilyMoreThenOneAdminService:
    def __init__(self, family_repository: FamilyRepository):
        self.family_repository = family_repository

    @logging(show_args=True, show_return=True)
    def execute(self, family_id: int):
        try:
            return self.__verify(family_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.GET_USER_FAMILY_ERROR.code())

    def __verify(self, family_id: int):
        family_entity = self.family_repository.find_admin_members(family_id)

        if family_entity is None or len(family_entity.members) <= 1:
            raise BadRequestError(code=BadRequestErrorCode.FAMILY_MUST_HAVE_AT_LEAST_ONE_ADMIN.code())
