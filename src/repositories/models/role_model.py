from sqlalchemy import Column, Integer, String

from src.domain.schemas.entity.role_entity import RoleEntity
from src.repositories.models import Base


class RoleModel(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def to_entity(self) -> RoleEntity:
        return RoleEntity(role_id=self.id, name=self.name)
