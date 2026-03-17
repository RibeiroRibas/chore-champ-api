from sqlalchemy import Column, Integer, String

from src.domain.entities.day_of_week_entity import DayOfWeekEntity
from src.repositories.models import Base


class DayOfWeekModel(Base):
    __tablename__ = "days_of_week"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(20), nullable=False)

    def to_entity(self) -> DayOfWeekEntity:
        return DayOfWeekEntity(id=self.id, name=self.name)
