from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.usecases.achievements.get_family_achievements_use_case import (
    GetFamilyAchievementsUseCase,
)
from src.infra.database.database import get_db
from src.repositories.achievement_repository import AchievementRepository
from src.repositories.user_repository import UserRepository


def get_family_achievements_use_case(
    db: Session = Depends(get_db),
) -> GetFamilyAchievementsUseCase:
    return GetFamilyAchievementsUseCase(
        achievement_repository=AchievementRepository(db_session=db),
        user_repository=UserRepository(db_session=db),
    )

