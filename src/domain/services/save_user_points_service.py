from src.application.schemas.users.add_user_points_dto import AddUserPointsDTO
from src.application.schemas.users.create_user_points_dto import CreateUserPointsDTO
from src.domain.entities.points_entity import PointsEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
from src.repositories.achievement_repository import AchievementRepository
from src.repositories.user_points_repository import UserPointsRepository
from src.repositories.user_achievement_repository import UserAchievementRepository


class SaveUserPointsService:
    def __init__(
        self,
        user_points_repository: UserPointsRepository,
        achievement_repository: AchievementRepository,
        user_achievement_repository: UserAchievementRepository,
    ):
        self.user_points_repository = user_points_repository
        self.achievement_repository = achievement_repository
        self.user_achievement_repository = user_achievement_repository

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
            new_available = existing.available_points() + dto.points
            self.__update(dto, existing)
            self.__sync_user_achievements(user_id=dto.user_id, available_points=new_available)
        else:
            new_available = dto.points
            self.__insert(dto)
            self.__sync_user_achievements(user_id=dto.user_id, available_points=new_available)

    def __insert(self, dto: AddUserPointsDTO):
        create_dto = CreateUserPointsDTO(
            user_id=dto.user_id,
            family_id=dto.family_id,
            total_points=dto.points,
        )
        self.user_points_repository.insert(dto=create_dto, commit=False)

    def __update(self, dto: AddUserPointsDTO, existing: PointsEntity):
        new_total = existing.total_points + dto.points
        self.user_points_repository.update_total_points(
            user_id=dto.user_id,
            total_points=new_total,
            commit=False,
        )

    def __sync_user_achievements(self, user_id: int, available_points: int) -> None:
        achievements = self.achievement_repository.find_all()
        for achievement in achievements:
            desired_times = available_points // achievement.required_points
            if desired_times <= 0:
                continue
            current_times = self.user_achievement_repository.count_by_user_and_achievement(
                user_id=user_id,
                achievement_id=achievement.id,
            )
            missing = desired_times - current_times
            if missing > 0:
                self.user_achievement_repository.insert_many(
                    user_id=user_id,
                    achievement_id=achievement.id,
                    amount=missing,
                    commit=False,
                )
