from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
from src.repositories.reward_repository import RewardRepository


class DeleteRewardUseCase:
    def __init__(self, reward_repository: RewardRepository):
        self.reward_repository = reward_repository

    @logging(show_args=True, show_return=True)
    def execute(self, reward_id: int) -> None:
        try:
            self.__delete_reward(reward_id=reward_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.DELETE_REWARD_ERROR.code())

    def __delete_reward(self, reward_id: int) -> None:
        self.reward_repository.delete_by_id(reward_id=reward_id)
