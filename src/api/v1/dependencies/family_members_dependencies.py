
from fastapi import Depends
from sqlalchemy.orm import Session

from src.api.middlewares.access_token_middleware import get_current_auth_id
from src.application.usecases.family.create_family_member_use_case import CreateFamilyMemberUseCase
from src.application.usecases.family.delete_family_member_use_case import DeleteFamilyMemberUseCase
from src.application.usecases.family.get_family_member_use_case import GetFamilyMemberUseCase
from src.application.usecases.users.has_permission_use_case import HasPermissionUseCase
from src.application.usecases.family.get_family_ranking_use_case import GetFamilyRankingUseCase
from src.application.usecases.family.list_family_members_use_case import ListFamilyMembersUseCase
from src.application.usecases.family.resend_family_member_password_use_case import (
    ResendFamilyMemberPasswordUseCase,
)
from src.application.usecases.family.update_family_member_use_case import UpdateFamilyMemberUseCase
from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.domain.enums.user_role_enum import UserRoleEnum
from src.domain.services.get_role_by_id_service import GetRoleByIdService
from src.domain.services.get_user_auth_family_service import GetUserAuthFamilyService
from src.domain.services.get_user_family_service import GetUserFamilyService
from src.domain.services.validate_family_has_more_then_one_admin_service import ValidateFamilyMoreThenOneAdminService
from src.infra.database.database import get_db
from src.repositories.auth_repository import AuthRepository
from src.repositories.family_repository import FamilyRepository
from src.repositories.role_repository import RoleRepository
from src.repositories.user_repository import UserRepository


def list_family_members_use_case(db: Session = Depends(get_db)) -> ListFamilyMembersUseCase:
    return ListFamilyMembersUseCase(family_repository=FamilyRepository(db_session=db))


def get_family_ranking_use_case(db: Session = Depends(get_db)) -> GetFamilyRankingUseCase:
    return GetFamilyRankingUseCase(user_repository=UserRepository(db_session=db))


def create_family_member_use_case(db: Session = Depends(get_db)) -> CreateFamilyMemberUseCase:
    role_repository = RoleRepository(db_session=db)
    return CreateFamilyMemberUseCase(
        user_repository=UserRepository(db_session=db),
        family_repository=FamilyRepository(db_session=db),
        auth_repository=AuthRepository(db_session=db),
        get_role_by_id_service=GetRoleByIdService(role_repository=role_repository),
    )


def get_family_member_use_case(db: Session = Depends(get_db)) -> GetFamilyMemberUseCase:
    user_repository = UserRepository(db_session=db)
    return GetFamilyMemberUseCase(
        user_repository=UserRepository(db_session=db),
        get_user_auth_family_service=GetUserAuthFamilyService(user_repository=user_repository),
    )


def update_family_member_use_case(db: Session = Depends(get_db)) -> UpdateFamilyMemberUseCase:
    user_repository = UserRepository(db_session=db)
    role_repository = RoleRepository(db_session=db)
    family_repository = FamilyRepository(db_session=db)
    return UpdateFamilyMemberUseCase(
        user_repository=UserRepository(db_session=db),
        auth_repository=AuthRepository(db_session=db),
        get_user_family_service=GetUserFamilyService(user_repository=user_repository),
        get_role_by_id_service=GetRoleByIdService(role_repository=role_repository),
        validate_family_has_more_then_one_admin_service=ValidateFamilyMoreThenOneAdminService(family_repository)
    )


def delete_family_member_use_case(db: Session = Depends(get_db)) -> DeleteFamilyMemberUseCase:
    user_repository = UserRepository(db_session=db)
    family_repository = FamilyRepository(db_session=db)
    return DeleteFamilyMemberUseCase(
        user_repository=UserRepository(db_session=db),
        auth_repository=AuthRepository(db_session=db),
        get_user_family_service=GetUserFamilyService(user_repository=user_repository),
        validate_family_has_more_then_one_admin_service=ValidateFamilyMoreThenOneAdminService(family_repository)
    )


def resend_family_member_password_use_case(db: Session = Depends(get_db)) -> ResendFamilyMemberPasswordUseCase:
    user_repository = UserRepository(db_session=db)
    return ResendFamilyMemberPasswordUseCase(
        auth_repository=AuthRepository(db_session=db),
        get_user_auth_family_service=GetUserAuthFamilyService(user_repository=user_repository),
    )
