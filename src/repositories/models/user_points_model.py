from sqlalchemy import Column, Integer, ForeignKey

from src.domain.schemas.entity.points_entity import PointsEntity
from src.repositories.models import Base


class UserPointsModel(Base):
    __tablename__ = "user_points"

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_points = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    points_redeemed = Column(Integer, nullable=False, default=0)
    family_id = Column(Integer, ForeignKey("families.id"), nullable=False)

    def to_entity(self) -> PointsEntity:
        return PointsEntity(
            id=self.id,
            total_points=self.total_points,
            user_id=self.user_id,
            points_redeemed=self.points_redeemed,
            family_id=self.family_id,
        )
