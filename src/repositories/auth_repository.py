from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.application.schemas.auth.create_auth_dto import CreateAuthDTO
from src.domain.entities.auth_entity import AuthEntity
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.not_found_error import NotFoundError
from src.repositories.models.auth_model import AuthModel


class AuthRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def insert(self, auth_dto: CreateAuthDTO, commit: bool = True) -> int:
        auth_model = AuthModel(username=auth_dto.username, password=auth_dto.password)
        self.db_session.add(auth_model)
        self.db_session.flush()
        if commit:
            self.db_session.commit()
        return auth_model.id

    def exists_by_email(self, email: str) -> bool:
        return self.db_session.query(AuthModel).filter_by(username=email).first() is not None

    def find_by_username(self, username: str) -> AuthEntity | None:
        model: AuthModel | None = self.db_session.query(AuthModel).filter_by(username=username).first()
        return model.to_entity() if model else None

    def update_password(self, password: str, auth_id: int, commit: bool = True):
        model: AuthModel | None = self.db_session.query(AuthModel).filter_by(id=auth_id).first()

        if model is None:
            raise NotFoundError(code=NotFoundErrorCodes.AUTH_NOT_FOUND.value)

        model.password = password
        model.updated_at = datetime.now(tz=timezone.utc)
        self.db_session.merge(model)

        if commit:
            self.db_session.commit()

    def update_username(self, auth_id: int, username: str, commit: bool = True) -> None:
        model: AuthModel | None = self.db_session.query(AuthModel).filter_by(id=auth_id).first()

        if model is None:
            raise NotFoundError(code=NotFoundErrorCodes.AUTH_NOT_FOUND.value)

        model.username = username
        model.updated_at = datetime.now(tz=timezone.utc)
        self.db_session.merge(model)
        if commit:
            self.db_session.commit()

    def find_by_id(self, auth_id: int) -> AuthEntity | None:
        model: AuthModel | None = self.db_session.query(AuthModel).filter_by(id=auth_id).first()
        return model.to_entity() if model else None

    def delete_by_id(self, auth_id: int, commit: bool = True) -> None:
        self.db_session.query(AuthModel).filter_by(id=auth_id).delete()
        if commit:
            self.db_session.commit()
