import unittest
from unittest.mock import MagicMock

from src.domain.entities.points_entity import PointsEntity
from src.domain.entities.reward_entity import RewardEntity
from src.domain.errors.internal_error import InternalError
from src.application.usecases.rewards.list_family_rewards_use_case import (
    ListFamilyRewardsUseCase,
)


class TestListFamilyRewardsUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_reward_repo = MagicMock()
        self.mock_points_repo = MagicMock()
        self.use_case = ListFamilyRewardsUseCase(
            reward_repository=self.mock_reward_repo,
            user_points_repository=self.mock_points_repo,
        )

    def test_execute_returns_empty_list_when_no_rewards(self):
        self.mock_reward_repo.find_all.return_value = []
        self.mock_points_repo.find_by_user_id.return_value = None
        result = self.use_case.execute(user_id=1)
        self.assertEqual(result, [])

    def test_execute_returns_responses_for_each_reward(self):
        rewards = [
            RewardEntity(
                reward_id=1,
                title="R1",
                subtitle=None,
                emoji="🎁",
                achievement_id=1,
                required_points=50,
            ),
        ]
        points = PointsEntity(
            id=1,
            total_points=100,
            user_id=1,
            points_redeemed=0,
            family_id=2,
        )
        self.mock_reward_repo.find_all.return_value = rewards
        self.mock_points_repo.find_by_user_id.return_value = points
        result = self.use_case.execute(user_id=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, 1)

    def test_execute_uses_zero_points_when_user_has_none(self):
        reward = RewardEntity(
            reward_id=1,
            title="R1",
            subtitle=None,
            emoji="🎁",
            achievement_id=1,
            required_points=50,
        )
        self.mock_reward_repo.find_all.return_value = [reward]
        self.mock_points_repo.find_by_user_id.return_value = None
        result = self.use_case.execute(user_id=1)
        self.assertEqual(len(result), 1)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError

        self.mock_reward_repo.find_all.side_effect = BadRequestError(code=400)
        with self.assertRaises(BadRequestError):
            self.use_case.execute(user_id=1)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_reward_repo.find_all.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.use_case.execute(user_id=1)
