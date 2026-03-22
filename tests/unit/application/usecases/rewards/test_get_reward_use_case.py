import unittest
from unittest.mock import MagicMock

from src.domain.schemas.entity.points_entity import PointsEntity
from src.domain.schemas.entity.reward_entity import RewardEntity
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.application.usecases.rewards.get_reward_use_case import GetRewardUseCase


class TestGetRewardUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_reward_repo = MagicMock()
        self.mock_points_repo = MagicMock()
        self.use_case = GetRewardUseCase(
            reward_repository=self.mock_reward_repo,
            user_points_repository=self.mock_points_repo,
        )

    def test_execute_returns_response_when_reward_found(self):
        reward = RewardEntity(
            reward_id=1,
            title="Recompensa",
            subtitle=None,
            emoji="🎁",
            achievement_id=1,
            required_points=50,
        )
        points = PointsEntity(
            id=1,
            total_points=100,
            user_id=1,
            points_redeemed=0,
            family_id=2,
        )
        self.mock_reward_repo.find_by_id.return_value = reward
        self.mock_points_repo.find_by_user_id.return_value = points
        result = self.use_case.execute(reward_id=1, user_id=1)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.title, "Recompensa")

    def test_execute_raises_not_found_when_reward_is_none(self):
        self.mock_reward_repo.find_by_id.return_value = None
        with self.assertRaises(NotFoundError):
            self.use_case.execute(reward_id=999, user_id=1)

    def test_execute_uses_zero_available_points_when_user_has_no_points(self):
        reward = RewardEntity(
            reward_id=1,
            title="Recompensa",
            subtitle=None,
            emoji="🎁",
            achievement_id=1,
            required_points=50,
        )
        self.mock_reward_repo.find_by_id.return_value = reward
        self.mock_points_repo.find_by_user_id.return_value = None
        result = self.use_case.execute(reward_id=1, user_id=1)
        self.assertEqual(result.id, 1)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError

        self.mock_reward_repo.find_by_id.side_effect = BadRequestError(code=400)
        with self.assertRaises(BadRequestError):
            self.use_case.execute(reward_id=1, user_id=1)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_reward_repo.find_by_id.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.use_case.execute(reward_id=1, user_id=1)
