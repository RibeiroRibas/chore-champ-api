from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.chore_user_entity import ChoreUserEntity
from src.repositories.models import Base


class ChoreModel(Base):
    __tablename__ = 'chores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    family_id = Column(Integer, ForeignKey('families.id'), nullable=False)
    title = Column(String, nullable=False)
    emoji = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    assigned_to_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
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
        )

    def to_chore_user_entity(self) -> ChoreUserEntity:
        return ChoreUserEntity(
            user_entity=self.assigned_to_user.to_entity() if self.assigned_to_user else None,
            chore=self.to_entity(),
        )
