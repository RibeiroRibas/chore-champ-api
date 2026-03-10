from src.domain.entities.role_entity import RoleEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.infra.decorators.logger import logging
from src.repositories.role_repository import RoleRepository


class GetRoleByIdService:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    @logging(show_args=True, show_return=True)
    def execute(self, role_id: int) -> RoleEntity:
        try:
            return self.__get_role(role_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.GET_CURRENT_USER_ERROR.code())

    def __get_role(self, role_id: int)-> RoleEntity:
        role: RoleEntity | None = self.role_repository.find_by_id(role_id)

        if role is None:
            raise NotFoundError(code=NotFoundErrorCodes.ROLE_NOT_FOUND.code())

        return role