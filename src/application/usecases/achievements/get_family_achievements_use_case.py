from collections import Counter

from src.api.v1.responses.achievements.achievement_response import AchievementResponse
from src.domain.schemas.entity.achievement_entity import AchievementEntity
from src.domain.schemas.entity.user_points_achievements_entity import UserPointsAchievementsEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.infra.decorators.logger import logging
from src.repositories.achievement_repository import AchievementRepository
from src.repositories.user_repository import UserRepository


class GetFamilyAchievementsUseCase:
    def __init__(
        self,
        achievement_repository: AchievementRepository,
        user_repository: UserRepository,
    ):
        self.achievement_repository = achievement_repository
        self.user_repository = user_repository

    @logging(show_args=True, show_return=True)
    def execute(self, user_id: int) -> list[AchievementResponse]:
        try:
            return self.__get_family_achievements(user_id=user_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.GET_FAMILY_ACHIEVEMENTS_ERROR.code())

    def __get_family_achievements(self, user_id: int) -> list[AchievementResponse]:
        entity: UserPointsAchievementsEntity | None = (
            self.user_repository.find_user_points_achievements(user_id)
        )
        if entity is None:
            raise NotFoundError(code=NotFoundErrorCodes.USER_NOT_FOUND.value())

        catalog: list[AchievementEntity] = self.achievement_repository.find_all()

        response: list[AchievementResponse] = []
        for achievement in catalog:
            acquired_times = entity.calculate_how_many_times_achievements_was_acquired(achievement)
            response.append(
                AchievementResponse.from_entity_with_acquired_times(entity=achievement, acquired_times=acquired_times)
            )
        return response

