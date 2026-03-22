from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func

from src.domain.schemas.entity.refresh_token_entity import RefreshTokenEntity
from src.repositories.models import Base


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    auth_id = Column(Integer, ForeignKey("auth.id"), nullable=False)
    refresh_token = Column(String(36), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def to_entity(self) -> RefreshTokenEntity:
        return RefreshTokenEntity(
            id=self.id,
            auth_id=self.auth_id,
            refresh_token=self.refresh_token,
            created_at=self.created_at,
        )
