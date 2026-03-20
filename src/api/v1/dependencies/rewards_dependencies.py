from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.usecases.rewards.claim_reward_use_case import ClaimRewardUseCase
from src.application.usecases.rewards.create_reward_use_case import CreateRewardUseCase
from src.application.usecases.rewards.delete_reward_use_case import DeleteRewardUseCase
from src.application.usecases.rewards.get_reward_use_case import GetRewardUseCase
from src.application.usecases.rewards.list_family_rewards_use_case import ListFamilyRewardsUseCase
from src.application.usecases.rewards.update_reward_use_case import UpdateRewardUseCase
from src.infra.database.database import get_db
from src.repositories.achievement_repository import AchievementRepository
from src.repositories.reward_repository import RewardRepository
from src.repositories.user_achievement_repository import UserAchievementRepository
from src.repositories.user_points_repository import UserPointsRepository


def list_family_rewards_use_case(db: Session = Depends(get_db)) -> ListFamilyRewardsUseCase:
    return ListFamilyRewardsUseCase(
        reward_repository=RewardRepository(db_session=db),
        user_points_repository=UserPointsRepository(db_session=db),
    )


def create_reward_use_case(db: Session = Depends(get_db)) -> CreateRewardUseCase:
    return CreateRewardUseCase(
        reward_repository=RewardRepository(db_session=db),
        achievement_repository=AchievementRepository(db_session=db),
        user_points_repository=UserPointsRepository(db_session=db),
    )


def get_reward_use_case(db: Session = Depends(get_db)) -> GetRewardUseCase:
    return GetRewardUseCase(
        reward_repository=RewardRepository(db_session=db),
        user_points_repository=UserPointsRepository(db_session=db),
    )


def update_reward_use_case(db: Session = Depends(get_db)) -> UpdateRewardUseCase:
    return UpdateRewardUseCase(
        reward_repository=RewardRepository(db_session=db),
        achievement_repository=AchievementRepository(db_session=db),
        user_points_repository=UserPointsRepository(db_session=db),
    )


def delete_reward_use_case(db: Session = Depends(get_db)) -> DeleteRewardUseCase:
    return DeleteRewardUseCase(
        reward_repository=RewardRepository(db_session=db),
    )


def claim_reward_use_case(db: Session = Depends(get_db)) -> ClaimRewardUseCase:
    return ClaimRewardUseCase(
        reward_repository=RewardRepository(db_session=db),
        user_points_repository=UserPointsRepository(db_session=db),
        user_achievement_repository=UserAchievementRepository(db_session=db),
    )
