from sqlalchemy.orm import Session

from src.domain.entities.achievement_entity import AchievementEntity
from src.repositories.models.achievement_model import AchievementModel


class AchievementRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_all(self) -> list[AchievementEntity]:
        models: list[AchievementModel] = (
            self.db_session.query(AchievementModel)
            .order_by(AchievementModel.required_points.asc())
            .all()
        )
        return [m.to_entity() for m in models]

