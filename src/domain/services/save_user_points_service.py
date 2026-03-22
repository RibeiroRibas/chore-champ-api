from src.domain.schemas.dto.users.add_user_points_dto import AddUserPointsDTO
from src.domain.schemas.dto.users.create_user_points_dto import CreateUserPointsDTO
from src.domain.schemas.entity.points_entity import PointsEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
from src.repositories.achievement_repository import AchievementRepository
from src.repositories.user_points_repository import UserPointsRepository


class SaveUserPointsService:
    def __init__(self, user_points_repository: UserPointsRepository,):
        self.user_points_repository = user_points_repository

    @logging(show_args=True, show_return=True)
    def execute(self, dto: AddUserPointsDTO) -> None:
        try:
            self.__save_or_update(dto)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.SAVE_USER_POINTS_ERROR.code())

    def __save_or_update(self, dto: AddUserPointsDTO) -> None:
        existing = self.user_points_repository.find_by_user_id(user_id=dto.user_id)
        if existing is not None:
            self.__update(dto, existing)
        else:
            self.__insert(dto)

    def __insert(self, dto: AddUserPointsDTO):
        create_dto = CreateUserPointsDTO(
            user_id=dto.user_id,
            family_id=dto.family_id,
            total_points=dto.points,
        )
        self.user_points_repository.insert(dto=create_dto)

    def __update(self, dto: AddUserPointsDTO, existing: PointsEntity):
        new_total = existing.total_points + dto.points
        self.user_points_repository.update_total_points(
            user_id=dto.user_id,
            total_points=new_total,
        )
