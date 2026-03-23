from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from src.domain.schemas.entity.achievement_entity import AchievementEntity
from src.repositories.models import Base


class UserAchievementModel(Base):
    __tablename__ = "c_user_achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("c_users.id", ondelete="CASCADE"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("c_achievements.id", ondelete="CASCADE"), nullable=False)
    acquired_at = Column(DateTime, server_default=func.now(), nullable=True)

    achievement =  relationship("AchievementModel", lazy="selectin")

    def to_achievement_entity(self) -> AchievementEntity:
        return self.achievement.to_entity()