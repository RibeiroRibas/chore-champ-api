from src.api.v1.responses.rewards.reward_response import RewardResponse
from src.domain.entities.points_entity import PointsEntity
from src.domain.entities.reward_entity import RewardEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.infra.decorators.logger import logging
from src.repositories.reward_repository import RewardRepository
from src.repositories.user_achievement_repository import UserAchievementRepository
from src.repositories.user_points_repository import UserPointsRepository


class ClaimRewardUseCase:
    def __init__(
        self,
        reward_repository: RewardRepository,
        user_points_repository: UserPointsRepository,
        user_achievement_repository: UserAchievementRepository,
    ):
        self.reward_repository = reward_repository
        self.user_points_repository = user_points_repository
        self.user_achievement_repository = user_achievement_repository

    @logging(show_args=True, show_return=True)
    def execute(self, reward_id: int, user_id: int) -> RewardResponse:
        try:
            return self.__claim_reward(reward_id=reward_id, user_id=user_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.CLAIM_REWARD_ERROR.code())

    def __claim_reward(self, reward_id: int, user_id: int) -> RewardResponse:
        reward: RewardEntity | None = self.reward_repository.find_by_id(reward_id=reward_id)
        if reward is None:
            raise NotFoundError(code=NotFoundErrorCodes.REWARD_NOT_FOUND.code())

        points: PointsEntity | None = self.user_points_repository.find_by_user_id(user_id=user_id)
        if points is None:
            raise NotFoundError(code=NotFoundErrorCodes.USER_POINTS_NOT_FOUND.code())

        required_points = reward.required_points or 0
        reward.validate_can_claim(available_points=points.available_points())

        self.user_points_repository.add_points_redeemed(
            user_id=user_id,
            points=required_points,
            commit=False,
        )
        self.user_achievement_repository.insert_many(
            user_id=user_id,
            achievement_id=reward.achievement_id,
            amount=1,
            commit=False,
        )
        self.user_points_repository.db_session.commit()

        refreshed_points = self.user_points_repository.find_by_user_id(user_id=user_id)
        available_points = refreshed_points.available_points() if refreshed_points else 0
        return RewardResponse.from_entity(entity=reward, available_points=available_points)
