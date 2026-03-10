from sqlalchemy.orm import Session

from src.repositories.models.role_model import RoleModel


class RoleRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_by_id(self, role_id: int) -> RoleModel | None:
        model: RoleModel | None = self.db_session.query(RoleModel).filter_by(id=role_id).first()
        return model.to_entity() if model else None
