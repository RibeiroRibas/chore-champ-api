from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.usecases.chores.create_chore_use_case import CreateChoreUseCase
from src.application.usecases.chores.delete_chore_use_case import DeleteChoreUseCase
from src.application.usecases.chores.get_chore_use_case import GetChoreUseCase
from src.application.usecases.chores.list_chores_use_case import ListChoresUseCase
from src.application.usecases.chores.update_chore_use_case import UpdateChoreUseCase
from src.domain.services.get_chore_user_service import GetChoreUSerService
from src.domain.services.get_user_family_service import GetUserFamilyService
from src.infra.database.database import get_db
from src.repositories.chore_repository import ChoreRepository
from src.repositories.user_repository import UserRepository


def list_chores_use_case(db: Session = Depends(get_db)) -> ListChoresUseCase:
    return ListChoresUseCase(chore_repository=ChoreRepository(db_session=db))


def create_chore_use_case(db: Session = Depends(get_db)) -> CreateChoreUseCase:
    user_repository = UserRepository(db_session=db)
    return CreateChoreUseCase(
        chore_repository=ChoreRepository(db_session=db),
        get_user_family_service=GetUserFamilyService(user_repository=user_repository),
    )


def get_chore_use_case(db: Session = Depends(get_db)) -> GetChoreUseCase:
    return GetChoreUseCase(chore_repository=ChoreRepository(db_session=db))


def update_chore_use_case(db: Session = Depends(get_db)) -> UpdateChoreUseCase:
    return UpdateChoreUseCase(
        chore_repository=ChoreRepository(db_session=db),
        get_chore_user_service=GetChoreUSerService(chore_repository=ChoreRepository(db_session=db)),
    )


def delete_chore_use_case(db: Session = Depends(get_db)) -> DeleteChoreUseCase:
    return DeleteChoreUseCase(chore_repository=ChoreRepository(db_session=db))
