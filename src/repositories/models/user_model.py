from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.entities.user_auth_family_entity import UserAuthFamilyEntity
from src.domain.entities.user_entity import UserEntity
from src.domain.entities.user_family_entity import UserFamilyEntity
from src.repositories.models import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    phone_number = Column(String, nullable=False)
    auth_id = Column(Integer, ForeignKey('auth.id'), nullable=False)
    family_id = Column(Integer, ForeignKey('families.id'), nullable=False)
    avatar = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    role = relationship("RoleModel", lazy="joined")
    family = relationship("FamilyModel", back_populates="members", lazy="selectin")
    auth = relationship("AuthModel", foreign_keys=[auth_id], lazy="selectin")

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            name=self.name,
            auth_id=self.auth_id,
            role=self.role.to_entity(),
            phone_number=self.phone_number,
            avatar=self.avatar,
        )

    def to_user_family_entity(self):
        return UserFamilyEntity(
            user_entity=self.to_entity(),
            family=self.family.to_entity(),
        )

    def to_current_user_entity(self):
        return CurrentUserEntity(
            user_id=self.id,
            auth_id=self.auth_id,
            role_id=self.role_id,
            family_id=self.family_id
        )

    def to_user_auth_family_entity(self):
        return UserAuthFamilyEntity(
            user_entity=self.to_entity(),
            family=self.family.to_entity(),
            auth_entity=self.auth.to_entity(),
        )
