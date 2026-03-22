from src.api.v1.responses.rewards.reward_response import RewardResponse
from src.domain.schemas.entity.points_entity import PointsEntity
from src.domain.schemas.entity.reward_entity import RewardEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.infra.decorators.logger import logging
from src.repositories.reward_repository import RewardRepository
from src.repositories.user_points_repository import UserPointsRepository


class GetRewardUseCase:
    def __init__(
        self,
        reward_repository: RewardRepository,
        user_points_repository: UserPointsRepository,
    ):
        self.reward_repository = reward_repository
        self.user_points_repository = user_points_repository

    @logging(show_args=True, show_return=True)
    def execute(self, reward_id: int, user_id: int) -> RewardResponse:
        try:
            return self.__get_reward(reward_id=reward_id, user_id=user_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.GET_REWARD_ERROR.code())

    def __get_reward(self, reward_id: int, user_id: int) -> RewardResponse:
        reward: RewardEntity | None = self.reward_repository.find_by_id(reward_id=reward_id)
        if reward is None:
            raise NotFoundError(code=NotFoundErrorCodes.REWARD_NOT_FOUND.code())

        points: PointsEntity | None = self.user_points_repository.find_by_user_id(user_id=user_id)
        available_points = points.available_points() if points else 0
        return RewardResponse.from_entity(entity=reward, available_points=available_points)
