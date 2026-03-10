from sqlalchemy import Column, Integer, String, DateTime, func

from src.domain.entities.auth_entity import AuthEntity
from src.repositories.models import Base


class AuthModel(Base):
    __tablename__ = 'auth'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    def to_entity(self) -> AuthEntity:
        return AuthEntity(
            id=self.id,
            username=self.username,
            password=self.password,
        )
