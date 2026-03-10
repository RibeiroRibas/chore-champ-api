from typing import List

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, Mapped

from src.domain.entities.family_entity import FamilyEntity
from src.repositories.models import Base, UserModel


class FamilyModel(Base):
    __tablename__ = 'families'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    members: Mapped[List["UserModel"]] = relationship(
        "UserModel",
        back_populates="family",
        lazy="selectin",
    )

    def to_entity(self) -> FamilyEntity:
        return FamilyEntity(
            id=self.id,
            name=self.name,
        )
