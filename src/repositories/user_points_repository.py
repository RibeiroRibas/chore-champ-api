from sqlalchemy.orm import Session

from src.application.schemas.users.create_user_points_dto import CreateUserPointsDTO
from src.domain.entities.points_entity import PointsEntity
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.not_found_error import NotFoundError
from src.repositories.models.user_points_model import UserPointsModel


class UserPointsRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_by_user_id(self, user_id: int) -> PointsEntity | None:
        model: UserPointsModel | None = (
            self.db_session.query(UserPointsModel).filter_by(user_id=user_id).first()
        )
        return model.to_entity() if model else None

    def insert(self, dto: CreateUserPointsDTO, commit: bool = True) -> PointsEntity:
        model = UserPointsModel(
            user_id=dto.user_id,
            family_id=dto.family_id,
            total_points=dto.total_points,
            points_redeemed=0,
        )
        self.db_session.add(model)
        if commit:
            self.db_session.commit()
            self.db_session.refresh(model)
        return model.to_entity()

    def update_total_points(self, user_id: int, total_points: int, commit: bool = True) -> PointsEntity:
        model: UserPointsModel | None = (
            self.db_session.query(UserPointsModel).filter_by(user_id=user_id).first()
        )
        if model is None:
            raise NotFoundError(code=NotFoundErrorCodes.USER_POINTS_NOT_FOUND.code())

        model.total_points = total_points
        if commit:
            self.db_session.commit()
            self.db_session.refresh(model)
        return model.to_entity()
