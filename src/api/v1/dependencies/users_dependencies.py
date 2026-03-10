from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.usecases.users.create_current_user_and_family_use_case import CreateCurrentUserAndFamilyUseCase
from src.application.usecases.users.get_current_user_use_case import GetCurrentUserUseCase
from src.application.usecases.users.update_current_user_use_case import UpdateCurrentUserUseCase
from src.infra.database.database import get_db
from src.repositories.family_repository import FamilyRepository
from src.repositories.user_repository import UserRepository


def create_current_user_and_family_use_case(db: Session = Depends(get_db)) -> CreateCurrentUserAndFamilyUseCase:
    user_repository = UserRepository(db_session=db)
    family_repository = FamilyRepository(db_session=db)
    return CreateCurrentUserAndFamilyUseCase(
        user_repository=user_repository,
        family_repository=family_repository,
    )

def get_current_user_use_case(db: Session = Depends(get_db)) -> GetCurrentUserUseCase:
    user_repository = UserRepository(db_session=db)
    return GetCurrentUserUseCase(user_repository=user_repository)

def update_current_user_use_case(db: Session = Depends(get_db)) -> UpdateCurrentUserUseCase:
    user_repository = UserRepository(db_session=db)
    return UpdateCurrentUserUseCase(user_repository=user_repository)
