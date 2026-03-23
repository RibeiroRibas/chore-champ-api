from typing import List

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.domain.schemas.entity.user_auth_family_entity import UserAuthFamilyEntity
from src.domain.schemas.entity.user_entity import UserEntity
from src.domain.schemas.entity.user_family_entity import UserFamilyEntity
from src.domain.schemas.entity.user_points_achievements_entity import UserPointsAchievementsEntity
from src.domain.schemas.entity.user_points_family_entity import UserPointsFamilyEntity
from src.repositories.models import Base

from src.repositories.models.chore_model import ChoreModel
from src.repositories.models.user_achievement_model import UserAchievementModel


class UserModel(Base):
    __tablename__ = 'c_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('c_roles.id'), nullable=False)
    phone_number = Column(String, nullable=False)
    auth_id = Column(Integer, ForeignKey('c_auth.id'), nullable=False)
    family_id = Column(Integer, ForeignKey('c_families.id'), nullable=False)
    avatar = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    role = relationship("RoleModel", lazy="joined")
    family = relationship("FamilyModel", back_populates="members", lazy="selectin")
    auth = relationship("AuthModel", foreign_keys=[auth_id], lazy="selectin")
    chores: Mapped[List["ChoreModel"]] = relationship(
        "ChoreModel",
        foreign_keys=[ChoreModel.assigned_to_user_id],
        back_populates="assigned_to_user",
        lazy="selectin",
    )
    user_points = relationship(
        "UserPointsModel",
        uselist=False,
        lazy="selectin",
    )
    achievements: Mapped[List["UserAchievementModel"]] = relationship(
        "UserAchievementModel",
        foreign_keys=[UserAchievementModel.user_id],
        lazy="selectin",
    )

    def to_entity(self) -> UserEntity:
        return UserEntity(
            user_id=self.id,
            name=self.name,
            auth_id=self.auth_id,
            role=self.role.to_entity(),
            phone_number=self.phone_number,
            avatar=self.avatar,
        )

    def to_user_family_entity(self) -> UserFamilyEntity:
        return UserFamilyEntity(
            user_entity=self.to_entity(),
            family=self.family.to_entity(),
        )

    def to_user_points_family_entity(self) -> UserPointsFamilyEntity:
        return UserPointsFamilyEntity(
            user=self.to_entity(),
            family=self.family.to_entity(),
            points=self.user_points.to_entity() if self.user_points else None,
        )

    def to_current_user_entity(self) ->CurrentUserEntity:
        return CurrentUserEntity(
            user_id=self.id,
            auth_id=self.auth_id,
            role_id=self.role_id,
            family_id=self.family_id
        )

    def to_user_auth_family_entity(self)-> UserAuthFamilyEntity:
        return UserAuthFamilyEntity(
            user_entity=self.to_entity(),
            family=self.family.to_entity(),
            auth_entity=self.auth.to_entity(),
        )

    def to_user_points_achievements(self)-> UserPointsAchievementsEntity:
        return UserPointsAchievementsEntity(
            user=self.to_entity(),
            points=self.user_points.to_entity() if self.user_points else None,
            achievements=[achievement.to_achievement_entity() for achievement in self.achievements] if self.achievements else None
        )
