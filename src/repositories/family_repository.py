from sqlalchemy.orm import Session, selectinload

from src.domain.entities.family_entity import FamilyEntity
from src.domain.entities.user_entity import UserEntity
from src.domain.enums.user_role_enum import UserRoleEnum
from src.repositories.models.family_model import FamilyModel
from src.repositories.models.user_model import UserModel


class FamilyRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def insert(self, name: str, commit: bool = True) -> int:
        family = FamilyModel(name=name)
        self.db_session.add(family)
        if commit:
            self.db_session.commit()
        else:
            self.db_session.flush()
        return family.id

    def find_by_id(self, family_id: int) -> FamilyEntity | None:
        model: FamilyModel | None = self.db_session.query(FamilyModel).filter_by(id=family_id).first()

        if model is None:
            return None

        return FamilyEntity(id=model.id, name=model.name)

    def find_by_id_with_members(self, family_id: int) -> FamilyEntity | None:
        model: FamilyModel | None = (
            self.db_session.query(FamilyModel)
            .options(
                selectinload(FamilyModel.members).selectinload(UserModel.role),
                selectinload(FamilyModel.members).selectinload(UserModel.auth),
            )
            .filter_by(id=family_id)
            .first()
        )
        if model is None:
            return None
        members = [
            UserEntity(
                user_id=member.id,
                name=member.name,
                auth_id=member.auth_id,
                role=member.role.to_entity(),
                phone_number=member.phone_number,
                email=member.auth.username if member.auth else None,
                avatar=member.avatar,
            )
            for member in model.members
        ]
        return FamilyEntity(id=model.id, name=model.name, members=members)

    def find_admin_members(self, family_id: int) -> FamilyEntity | None:
        model: FamilyModel | None = (
            self.db_session.query(FamilyModel)
            .options(selectinload(FamilyModel.members).selectinload(UserModel.role))
            .filter_by(id=family_id)
            .first()
        )
        if model is None:
            return None
        members = [
            UserEntity(
                user_id=member.id,
                name=member.name,
                auth_id=member.auth_id,
                role=member.role.to_entity(),
                phone_number=member.phone_number,
                email=member.auth.username if member.auth else None,
                avatar=member.avatar,
            )
            for member in model.members if member.role.to_entity().get_role() == UserRoleEnum.ADMIN
        ]
        return FamilyEntity(id=model.id, name=model.name, members=members)
