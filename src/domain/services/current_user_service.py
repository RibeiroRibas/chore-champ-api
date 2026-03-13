from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.not_found_error import NotFoundError
from src.repositories.user_repository import UserRepository


def get_current_user_by_auth_id(auth_id: int, user_repository: UserRepository) -> CurrentUserEntity:
    user = user_repository.find_current_user_by_auth_id(auth_id)

    if user is None:
        raise NotFoundError(code=NotFoundErrorCodes.CURRENT_USER_NOT_FOUND.code())

    return user