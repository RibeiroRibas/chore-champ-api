from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.usecases.chores.assign_chore_to_me_use_case import AssignChoreToMeUseCase
from src.application.usecases.chores.complete_chore_use_case import CompleteChoreUseCase
from src.application.usecases.chores.create_chore_use_case import CreateChoreUseCase
from src.application.usecases.chores.delete_chore_use_case import DeleteChoreUseCase
from src.application.usecases.chores.get_chore_use_case import GetChoreUseCase
from src.application.usecases.chores.list_all_chores_use_case import ListAllChoresUseCase
from src.application.usecases.chores.list_today_chores_use_case import ListTodayChoresUseCase
from src.application.usecases.chores.remove_assign_chore_to_me_use_case import RemoveAssignChoreToMeUseCase
from src.application.usecases.chores.update_chore_use_case import UpdateChoreUseCase
from src.domain.services.create_chore_service import CreateChoreService
from src.domain.services.detect_new_reward_unlocked_service import (
    DetectNewRewardUnlockedService,
)
from src.domain.services.get_chore_service import GetChoreService
from src.domain.services.get_chore_user_service import GetChoreUSerService
from src.domain.services.list_today_chore_entities_service import (
    ListTodayChoreEntitiesService,
)
from src.domain.services.recurring_chore_service import RecurringChoreService
from src.domain.services.save_user_points_service import SaveUserPointsService
from src.infra.database.database import get_db
from src.repositories.chore_repository import ChoreRepository
from src.repositories.recurring_chore_repository import RecurringChoreRepository
from src.repositories.reward_repository import RewardRepository
from src.repositories.user_points_repository import UserPointsRepository


def list_today_chores_use_case(db: Session = Depends(get_db)) -> ListTodayChoresUseCase:
    chore_repository = ChoreRepository(db_session=db)
    recurring_chore_repository = RecurringChoreRepository(db_session=db)
    list_today_service = ListTodayChoreEntitiesService(
        chore_repository=chore_repository,
        recurring_chore_repository=recurring_chore_repository,
    )
    return ListTodayChoresUseCase(
        list_today_chore_entities_service=list_today_service,
    )


def list_all_chores_use_case(db: Session = Depends(get_db)) -> ListAllChoresUseCase:
    return ListAllChoresUseCase(chore_repository=ChoreRepository(db_session=db))


def create_chore_use_case(db: Session = Depends(get_db)) -> CreateChoreUseCase:
    chore_repository = ChoreRepository(db_session=db)
    recurring_chore_repository = RecurringChoreRepository(db_session=db)
    recurring_chore_service = RecurringChoreService(recurring_chore_repository)
    user_points_repository = UserPointsRepository(db_session=db)
    save_user_points_service = SaveUserPointsService(
        user_points_repository=user_points_repository,
    )
    detect = DetectNewRewardUnlockedService(
        reward_repository=RewardRepository(db_session=db),
        user_points_repository=user_points_repository,
    )
    create_chore_service = CreateChoreService(
        chore_repository=chore_repository,
        recurring_chore_service=recurring_chore_service,
        save_user_points_service=save_user_points_service,
        detect_new_reward_unlocked_service=detect,
    )
    return CreateChoreUseCase(
        create_chore_service=create_chore_service,
    )


def get_chore_use_case(db: Session = Depends(get_db)) -> GetChoreUseCase:
    return GetChoreUseCase(chore_repository=ChoreRepository(db_session=db))


def update_chore_use_case(db: Session = Depends(get_db)) -> UpdateChoreUseCase:
    chore_repository = ChoreRepository(db_session=db)
    recurring_chore_repository = RecurringChoreRepository(db_session=db)
    user_points_repository = UserPointsRepository(db_session=db)
    recurring_chore_service = RecurringChoreService(
        recurring_chore_repository=recurring_chore_repository,
    )
    save_user_points_service = SaveUserPointsService(
        user_points_repository=user_points_repository,
    )
    list_today_service = ListTodayChoreEntitiesService(
        chore_repository=chore_repository,
        recurring_chore_repository=recurring_chore_repository,
    )
    detect = DetectNewRewardUnlockedService(
        reward_repository=RewardRepository(db_session=db),
        user_points_repository=user_points_repository,
    )
    create_chore_service = CreateChoreService(
        chore_repository=chore_repository,
        recurring_chore_service=recurring_chore_service,
        save_user_points_service=save_user_points_service,
        detect_new_reward_unlocked_service=detect,
    )
    return UpdateChoreUseCase(
        chore_repository=chore_repository,
        get_chore_service=GetChoreService(chore_repository=chore_repository),
        recurring_chore_service=recurring_chore_service,
        save_user_points_service=save_user_points_service,
        list_today_chore_entities_service=list_today_service,
        detect_new_reward_unlocked_service=detect,
        create_chore_use_case=create_chore_service
    )


def delete_chore_use_case(db: Session = Depends(get_db)) -> DeleteChoreUseCase:
    repository = ChoreRepository(db_session=db)
    get_chore_user_service = GetChoreUSerService(chore_repository=repository)
    recurring_chore_repository = RecurringChoreRepository(db_session=db)
    recurring_chore_service = RecurringChoreService(
        recurring_chore_repository=recurring_chore_repository,
    )
    return DeleteChoreUseCase(chore_repository=repository, get_chore_user_service=get_chore_user_service,
                              recurring_chore_service=recurring_chore_service)


def assign_chore_to_me_use_case(db: Session = Depends(get_db)) -> AssignChoreToMeUseCase:
    repository = ChoreRepository(db_session=db)
    get_chore_service = GetChoreService(chore_repository=repository)
    return AssignChoreToMeUseCase(
        chore_repository=repository,
        get_chore_service=get_chore_service,
    )


def remove_assign_chore_to_me_use_case(db: Session = Depends(get_db)) -> RemoveAssignChoreToMeUseCase:
    repository = ChoreRepository(db_session=db)
    get_chore_service = GetChoreService(chore_repository=repository)
    return RemoveAssignChoreToMeUseCase(
        chore_repository=repository,
        get_chore_service=get_chore_service,
    )


def complete_chore_use_case(db: Session = Depends(get_db)) -> CompleteChoreUseCase:
    chore_repository = ChoreRepository(db_session=db)
    recurring_chore_repository = RecurringChoreRepository(db_session=db)
    user_points_repository = UserPointsRepository(db_session=db)
    recurring_chore_service = RecurringChoreService(
        recurring_chore_repository=recurring_chore_repository,
    )
    save_user_points_service = SaveUserPointsService(
        user_points_repository=user_points_repository,
    )
    list_today_service = ListTodayChoreEntitiesService(
        chore_repository=chore_repository,
        recurring_chore_repository=recurring_chore_repository,
    )
    detect = DetectNewRewardUnlockedService(
        reward_repository=RewardRepository(db_session=db),
        user_points_repository=user_points_repository,
    )
    create_chore_service = CreateChoreService(
        chore_repository=chore_repository,
        recurring_chore_service=recurring_chore_service,
        save_user_points_service=save_user_points_service,
        detect_new_reward_unlocked_service=detect,
    )
    return CompleteChoreUseCase(
        chore_repository=chore_repository,
        get_chore_service=GetChoreService(chore_repository=chore_repository),
        recurring_chore_service=recurring_chore_service,
        save_user_points_service=save_user_points_service,
        list_today_chore_entities_service=list_today_service,
        detect_new_reward_unlocked_service=detect,
        creat_chore_service=create_chore_service,
    )
