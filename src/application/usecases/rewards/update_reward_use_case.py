from src.api.v1.requests.rewards.update_reward_request import UpdateRewardRequest
from src.api.v1.responses.rewards.reward_response import RewardResponse
from src.application.schemas.rewards.update_reward_dto import UpdateRewardDTO
from src.domain.entities.achievement_entity import AchievementEntity
from src.domain.entities.points_entity import PointsEntity
from src.domain.entities.reward_entity import RewardEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.infra.decorators.logger import logging
from src.repositories.achievement_repository import AchievementRepository
from src.repositories.reward_repository import RewardRepository
from src.repositories.user_points_repository import UserPointsRepository


class UpdateRewardUseCase:
    def __init__(
        self,
        reward_repository: RewardRepository,
        achievement_repository: AchievementRepository,
        user_points_repository: UserPointsRepository,
    ):
        self.reward_repository = reward_repository
        self.achievement_repository = achievement_repository
        self.user_points_repository = user_points_repository

    @logging(show_args=True, show_return=True)
    def execute(self, reward_id: int, request: UpdateRewardRequest, user_id: int) -> RewardResponse:
        try:
            return self.__update_reward(reward_id=reward_id, request=request, user_id=user_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.UPDATE_REWARD_ERROR.code())

    def __update_reward(self, reward_id: int, request: UpdateRewardRequest, user_id: int) -> RewardResponse:
        self.__validate_achievement_exists(achievement_id=request.achievement_id)
        dto = UpdateRewardDTO(
            title=request.title,
            subtitle=request.subtitle,
            emoji=request.emoji,
            achievement_id=request.achievement_id,
        )
        reward: RewardEntity = self.reward_repository.update(reward_id=reward_id, dto=dto)
        points: PointsEntity | None = self.user_points_repository.find_by_user_id(user_id=user_id)
        available_points = points.available_points() if points else 0
        return RewardResponse.from_entity(entity=reward, available_points=available_points)

    def __validate_achievement_exists(self, achievement_id: int) -> None:
        achievement: AchievementEntity | None = self.achievement_repository.find_by_id(achievement_id=achievement_id)
        if achievement is None:
            raise NotFoundError(code=NotFoundErrorCodes.ACHIEVEMENT_NOT_FOUND.code())
