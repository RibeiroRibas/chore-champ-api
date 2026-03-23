from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from src.domain.schemas.entity.recurring_chore_entity import RecurringChoreEntity
from src.repositories.models import Base


class RecurringChoreModel(Base):
    __tablename__ = "c_recurring_chores"

    chore_id = Column(Integer, ForeignKey("c_chores.id", ondelete="CASCADE"), nullable=False)
    day_of_week_id = Column(Integer, ForeignKey("c_days_of_week.id"), nullable=False)
    family_id = Column(Integer, ForeignKey('c_families.id'), nullable=False)
    parent_chore_id = Column(Integer, ForeignKey("c_chores.id", ondelete="CASCADE"), nullable=True)

    __table_args__ = (PrimaryKeyConstraint("chore_id", "day_of_week_id"),)

    day_of_week = relationship("DayOfWeekModel", lazy="selectin")

    def to_entity(self) -> RecurringChoreEntity:
        return RecurringChoreEntity(
            chore_id=self.chore_id,
            day_of_week=self.day_of_week.to_entity(),
            parent_chore_id=self.parent_chore_id,
        )
