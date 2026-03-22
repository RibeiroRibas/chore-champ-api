from fastapi import Depends
from sqlalchemy.orm import Session

from src.api.middlewares.access_token_middleware import get_current_auth_id
from src.application.usecases.users.has_permission_use_case import HasPermissionUseCase
from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.domain.enums.user_role_enum import UserRoleEnum
from src.domain.services import current_user_service
from src.infra.database.database import get_db
from src.repositories.user_repository import UserRepository


def has_permission_admin_use_case(db: Session = Depends(get_db), auth_id: int = Depends(get_current_auth_id))-> CurrentUserEntity:
    user_repository = UserRepository(db_session=db)
    return HasPermissionUseCase(role=UserRoleEnum.ADMIN, repository=user_repository).call(auth_id=auth_id)

def get_current_user_entity(
    auth_id: int = Depends(get_current_auth_id),
    db: Session = Depends(get_db),
) -> CurrentUserEntity:
    user_repository = UserRepository(db_session=db)
    return current_user_service.get_current_user_by_auth_id(auth_id=auth_id, user_repository=user_repository)