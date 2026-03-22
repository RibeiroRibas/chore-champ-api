from sqlalchemy.orm import Session

from src.domain.schemas.entity.refresh_token_entity import RefreshTokenEntity
from src.repositories.models.refresh_token_model import RefreshTokenModel


class RefreshTokenRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def insert(self, auth_id: int, refresh_token: str, commit: bool = True):
        model = RefreshTokenModel(auth_id=auth_id, refresh_token=refresh_token)
        self.db_session.add(model)
        self.db_session.flush()
        if commit:
            self.db_session.commit()

    def find_by_refresh_token_and_auth_id(self, refresh_token: str, auth_id: int) -> RefreshTokenEntity | None:
        model: RefreshTokenModel | None = (
            self.db_session.query(RefreshTokenModel)
            .filter_by(refresh_token=refresh_token)
            .filter_by(auth_id=auth_id)
            .first()
        )
        return model.to_entity() if model else None

    def delete_by_auth_id(self, auth_id: int, commit: bool = True) -> None:
        self.db_session.query(RefreshTokenModel).filter_by(auth_id=auth_id).delete()
        if commit:
            self.db_session.commit()
