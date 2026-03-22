from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.domain.schemas.entity.reward_entity import RewardEntity
from src.repositories.models import Base


class RewardModel(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=True)
    emoji = Column(String, nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)

    achievement = relationship("AchievementModel", lazy="selectin")

    def to_entity(self) -> RewardEntity:
        return RewardEntity(
            reward_id=self.id,
            title=self.title,
            subtitle=self.subtitle,
            emoji=self.emoji,
            achievement_id=self.achievement_id,
            required_points=self.achievement.required_points if self.achievement else None,
        )
