from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.schemas.entity.chore_entity import ChoreEntity
from src.domain.schemas.entity.chore_user_entity import ChoreUserEntity
from src.repositories.models import Base
from src.repositories.models.recurring_chore_model import RecurringChoreModel


class ChoreModel(Base):
    __tablename__ = 'c_chores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    family_id = Column(Integer, ForeignKey('c_families.id'), nullable=False)
    title = Column(String, nullable=False)
    emoji = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    assigned_to_user_id = Column(Integer, ForeignKey('c_users.id'), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey('c_users.id'), nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    completed_at = Column(DateTime, nullable=True)
    is_recurring = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    family = relationship("FamilyModel", back_populates="chores", lazy="selectin")
    assigned_to_user = relationship(
        "UserModel",
        foreign_keys=[assigned_to_user_id],
        back_populates="chores",
        lazy="selectin",
    )
    created_by_user = relationship(
        "UserModel",
        foreign_keys=[created_by_user_id],
        lazy="selectin",
    )
    chore_days = relationship(
        "RecurringChoreModel",
        foreign_keys=[RecurringChoreModel.chore_id],
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def to_entity(self) -> ChoreEntity:
        return ChoreEntity(
            chore_id=self.id,
            family_id=self.family_id,
            title=self.title,
            emoji=self.emoji,
            points=self.points,
            assigned_to_user_id=self.assigned_to_user_id,
            created_by_user_id=self.created_by_user_id,
            completed=self.completed,
            is_recurring=self.is_recurring,
            recurrence_days=[cd.day_of_week.to_entity() for cd in self.chore_days],
        )

    def to_chore_user_entity(self) -> ChoreUserEntity:
        return ChoreUserEntity(
            user_entity=self.assigned_to_user.to_entity() if self.assigned_to_user else None,
            chore=self.to_entity(),
        )
