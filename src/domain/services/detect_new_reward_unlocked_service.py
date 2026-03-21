from collections.abc import Callable

from src.domain.entities.new_reward_unlock_check_entity import NewRewardUnlockCheckEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
from src.repositories.reward_repository import RewardRepository
from src.repositories.user_points_repository import UserPointsRepository


class DetectNewRewardUnlockedService:
    def __init__(
        self,
        reward_repository: RewardRepository,
        user_points_repository: UserPointsRepository,
    ):
        self.__reward_repository = reward_repository
        self.__user_points_repository = user_points_repository

    @logging(show_args=True, show_return=True)
    def execute(
        self,
        user_id: int | None,
        mutate_points: Callable[[], None],
    ) -> NewRewardUnlockCheckEntity:
        try:
            return self.__execute(user_id=user_id, mutate_points=mutate_points)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.DETECT_NEW_REWARD_UNLOCKED_SERVICE_ERROR.code())

    def __execute(
        self,
        user_id: int | None,
        mutate_points: Callable[[], None],
    ) -> NewRewardUnlockCheckEntity:
        before = self.__available_points(user_id=user_id)
        mutate_points()
        after = self.__available_points(user_id=user_id)
        unlocked = self.__new_reward_unlocked(
            available_points_before=before,
            available_points_after=after,
        )
        return NewRewardUnlockCheckEntity(
            available_points_before=before,
            available_points_after=after,
            new_reward_unlocked=unlocked,
        )

    def __available_points(self, user_id: int | None) -> int:
        if user_id is None:
            return 0
        row = self.__user_points_repository.find_by_user_id(user_id=user_id)
        return row.available_points() if row is not None else 0

    def __new_reward_unlocked(self, available_points_before: int, available_points_after: int) -> bool:
        if available_points_after <= available_points_before:
            return False

        rewards = self.__reward_repository.find_all()
        for reward in rewards:
            required = reward.required_points
            if required is None:
                continue
            was_locked = not reward.is_unlocked(available_points=available_points_before)
            now_unlocked = reward.is_unlocked(available_points=available_points_after)
            if was_locked and now_unlocked:
                return True

        return False
