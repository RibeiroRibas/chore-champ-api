from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, SMALLINT

from src.domain.schemas.entity.email_code_checking_entity import EmailCodeCheckingEntity
from src.repositories.models import Base


class EmailCodeCheckingModel(Base):
    __tablename__ = 'email_code_checking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(SMALLINT, nullable=False)
    is_code_blocked = Column(Boolean, nullable=False, default=False)
    validated = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    validation_attempts = Column(Integer, nullable=False, default=0)

    def to_entity(self) -> EmailCodeCheckingEntity:
        return EmailCodeCheckingEntity(
            id=self.id,
            email=self.email,
            code=self.code,
            is_blocked=self.is_code_blocked,
            validated=self.validated,
            validation_attempts=self.validation_attempts,
            created_at=self.created_at
        )

    @staticmethod
    def from_entity(entity: EmailCodeCheckingEntity):
        return EmailCodeCheckingModel(
            id=entity.id,
            email=entity.email,
            code=entity.code,
            is_code_blocked=entity.is_blocked,
            validated=entity.validated,
            validation_attempts=entity.validation_attempts,
            created_at=entity.created_at,
            updated_at=func.now()
        )
