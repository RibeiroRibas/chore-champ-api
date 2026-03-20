from src.api.v1.responses.rewards.reward_response import RewardResponse
from src.domain.entities.points_entity import PointsEntity
from src.domain.entities.reward_entity import RewardEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
from src.repositories.reward_repository import RewardRepository
from src.repositories.user_points_repository import UserPointsRepository


class ListFamilyRewardsUseCase:
    def __init__(
        self,
        reward_repository: RewardRepository,
        user_points_repository: UserPointsRepository,
    ):
        self.reward_repository = reward_repository
        self.user_points_repository = user_points_repository

    @logging(show_args=True, show_return=True)
    def execute(self, user_id: int) -> list[RewardResponse]:
        try:
            return self.__list_rewards(user_id=user_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.LIST_REWARDS_ERROR.code())

    def __list_rewards(self, user_id: int) -> list[RewardResponse]:
        points: PointsEntity | None = self.user_points_repository.find_by_user_id(user_id=user_id)
        available_points = points.available_points() if points else 0
        rewards: list[RewardEntity] = self.reward_repository.find_all()
        return [
            RewardResponse.from_entity(entity=reward, available_points=available_points)
            for reward in rewards
        ]
