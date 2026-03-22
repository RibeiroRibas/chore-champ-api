from sqlalchemy.orm import Session

from src.domain.schemas.entity.day_of_week_entity import DayOfWeekEntity
from src.repositories.models.day_of_week_model import DayOfWeekModel


class DayOfWeekRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_all(self) -> list[DayOfWeekEntity]:
        models: list[DayOfWeekModel] = (
            self.db_session.query(DayOfWeekModel)
            .order_by(DayOfWeekModel.id)
            .all()
        )
        return [m.to_entity() for m in models]
