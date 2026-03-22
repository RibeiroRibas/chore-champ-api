from sqlalchemy import Column, Integer, String, DateTime, func

from src.domain.schemas.entity.achievement_entity import AchievementEntity
from src.repositories.models import Base


class AchievementModel(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    emoji = Column(String, nullable=False)
    required_points = Column(Integer, nullable=False)

    def to_entity(self) -> AchievementEntity:
        return AchievementEntity(
            achievement_id=self.id,
            title=self.title,
            description=self.description,
            emoji=self.emoji,
            required_points=self.required_points,
        )

