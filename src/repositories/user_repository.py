from sqlalchemy.orm import Session

from src.domain.schemas.dto.users.create_user_dto import CreateUserDTO
from src.domain.schemas.dto.users.update_user_dto import UpdateUserDTO
from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.domain.schemas.entity.family_member_ranking_entity import FamilyMemberRankingEntity
from src.domain.schemas.entity.user_auth_family_entity import UserAuthFamilyEntity
from src.domain.schemas.entity.user_entity import UserEntity
from src.domain.schemas.entity.user_family_entity import UserFamilyEntity
from src.domain.schemas.entity.user_points_achievements_entity import UserPointsAchievementsEntity
from src.domain.schemas.entity.user_points_family_entity import UserPointsFamilyEntity
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.not_found_error import NotFoundError
from src.repositories.models.user_model import UserModel


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def insert(self, user_dto: CreateUserDTO, commit: bool = True) -> int:
        user_model = UserModel(
            name=user_dto.name,
            auth_id=user_dto.auth_id,
            role_id=user_dto.role_id,
            phone_number=user_dto.phone.digits,
            family_id=user_dto.family_id,
            avatar=user_dto.avatar,
        )
        self.db_session.add(user_model)
        self.db_session.flush()
        if commit:
            self.db_session.commit()
        return user_model.id

    def exists_by_auth_id(self, auth_id: int) -> bool:
        return self.db_session.query(UserModel).filter_by(auth_id=auth_id).first() is not None

    def find_current_user_by_auth_id(self, auth_id: int) -> CurrentUserEntity | None:
        model: UserModel | None = self.db_session.query(UserModel).filter_by(auth_id=auth_id).first()
        return model.to_current_user_entity() if model else None

    def find_by_auth_id_with_family_and_points(
        self, auth_id: int
    ) -> UserPointsFamilyEntity | None:
        model: UserModel | None = (
            self.db_session.query(UserModel).filter_by(auth_id=auth_id).first()
        )
        return model.to_user_points_family_entity() if model else None

    def find_by_id(self, user_id: int) -> UserEntity | None:
        model: UserModel | None = self.db_session.query(UserModel).filter_by(id=user_id).first()
        return model.to_entity() if model else None

    def find_by_id_with_family(self, user_id: int) -> UserFamilyEntity | None:
        model: UserModel | None = self.db_session.query(UserModel).filter_by(id=user_id).first()
        return model.to_user_family_entity() if model else None

    def find_by_id_with_auth_and_family(self, user_id: int) -> UserAuthFamilyEntity | None:
        model: UserModel | None = self.db_session.query(UserModel).filter_by(id=user_id).first()
        return model.to_user_auth_family_entity() if model else None

    def find_user_points_achievements(self, user_id: int) -> UserPointsAchievementsEntity | None:
        model: UserModel | None = self.db_session.query(UserModel).filter_by(id=user_id).first()
        return model.to_user_points_achievements() if model else None

    def find_ranking_by_family_id(self, family_id: int) -> list[FamilyMemberRankingEntity]:
        models: list[UserModel] | None = (
            self.db_session.query(UserModel)
            .filter_by(family_id=family_id)
            .all()
        )
        if not models:
            return []
        result: list[FamilyMemberRankingEntity] = []
        for m in models:
            points = (
                m.user_points.to_entity().available_points()
                if m.user_points
                else 0
            )
            result.append(
                FamilyMemberRankingEntity(
                    id=m.id,
                    name=m.name,
                    points=points,
                    role_name=m.role.name,
                    avatar=m.avatar or "👤",
                )
            )
        result.sort(key=lambda e: e.points, reverse=True)
        return result

    def delete_by_id(self, user_id: int, commit: bool = True) -> None:
        self.db_session.query(UserModel).filter_by(id=user_id).delete()
        if commit:
            self.db_session.commit()

    def update(self, user_dto: UpdateUserDTO, user_id: int,  commit: bool = True):
        model: UserModel | None = self.db_session.query(UserModel).filter_by(id=user_id).first()

        if not model:
            raise NotFoundError(code=NotFoundErrorCodes.USER_NOT_FOUND.value())

        model.name = user_dto.name
        model.phone_number = user_dto.phone.digits
        if user_dto.avatar is not None:
            model.avatar = user_dto.avatar
        self.db_session.merge(model)
        if commit:
            self.db_session.commit()
