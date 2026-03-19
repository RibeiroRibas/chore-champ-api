from sqlalchemy import func
from sqlalchemy.orm import Session

from src.repositories.models.user_achievement_model import UserAchievementModel


class UserAchievementRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def count_by_user_and_achievement(
        self,
        *,
        user_id: int,
        achievement_id: int,
    ) -> int:
        result = (
            self.db_session.query(func.count(UserAchievementModel.id))
            .filter_by(user_id=user_id, achievement_id=achievement_id)
            .scalar()
        )
        return int(result or 0)

    def count_grouped_by_achievement_id(self, *, user_id: int) -> dict[int, int]:
        rows = (
            self.db_session.query(
                UserAchievementModel.achievement_id,
                func.count(UserAchievementModel.id),
            )
            .filter_by(user_id=user_id)
            .group_by(UserAchievementModel.achievement_id)
            .all()
        )
        return {int(achievement_id): int(count) for achievement_id, count in rows}

    def insert_many(
        self,
        *,
        user_id: int,
        achievement_id: int,
        amount: int,
        commit: bool = True,
    ) -> None:
        if amount <= 0:
            return
        items = [
            UserAchievementModel(
                user_id=user_id,
                achievement_id=achievement_id,
            )
            for _ in range(amount)
        ]
        self.db_session.add_all(items)
        if commit:
            self.db_session.commit()

