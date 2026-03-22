from sqlalchemy.orm import Session

from src.domain.schemas.entity.achievement_entity import AchievementEntity
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

    def find_by_id(self, achievement_id: int) -> AchievementEntity | None:
        model: AchievementModel | None = (
            self.db_session.query(AchievementModel).filter_by(id=achievement_id).first()
        )
        return model.to_entity() if model else None

