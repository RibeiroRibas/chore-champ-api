import unittest
from unittest.mock import MagicMock

from src.domain.entities.new_reward_unlock_check_entity import NewRewardUnlockCheckEntity
from src.domain.entities.reward_entity import RewardEntity
from src.domain.errors.internal_error import InternalError
from src.domain.services.detect_new_reward_unlocked_service import (
    DetectNewRewardUnlockedService,
)


class TestDetectNewRewardUnlockedService(unittest.TestCase):
    def setUp(self):
        self.mock_reward_repo = MagicMock()
        self.mock_points_repo = MagicMock()
        self.service = DetectNewRewardUnlockedService(
            reward_repository=self.mock_reward_repo,
            user_points_repository=self.mock_points_repo,
        )

    def test_execute_returns_false_when_user_id_is_none_and_no_mutation(self):
        def noop():
            pass

        result = self.service.execute(user_id=None, mutate_points=noop)
        self.assertIsInstance(result, NewRewardUnlockCheckEntity)
        self.assertEqual(result.available_points_before, 0)
        self.assertEqual(result.available_points_after, 0)
        self.assertFalse(result.new_reward_unlocked)
        self.mock_points_repo.find_by_user_id.assert_not_called()

    def test_execute_returns_false_when_points_do_not_increase(self):
        points_row = MagicMock()
        points_row.available_points.return_value = 100
        self.mock_points_repo.find_by_user_id.return_value = points_row
        self.mock_reward_repo.find_all.return_value = []

        def noop():
            pass

        result = self.service.execute(user_id=1, mutate_points=noop)
        self.assertEqual(result.available_points_before, 100)
        self.assertEqual(result.available_points_after, 100)
        self.assertFalse(result.new_reward_unlocked)

    def test_execute_returns_true_when_reward_unlocks_after_points_increase(self):
        self.mock_points_repo.find_by_user_id.side_effect = [
            MagicMock(available_points=MagicMock(return_value=50)),
            MagicMock(available_points=MagicMock(return_value=150)),
        ]
        reward = RewardEntity(
            reward_id=1,
            title="Test",
            subtitle=None,
            emoji="🎁",
            achievement_id=1,
            required_points=100,
        )
        self.mock_reward_repo.find_all.return_value = [reward]

        def mutate():
            pass

        result = self.service.execute(user_id=1, mutate_points=mutate)
        self.assertEqual(result.available_points_before, 50)
        self.assertEqual(result.available_points_after, 150)
        self.assertTrue(result.new_reward_unlocked)

    def test_execute_returns_false_when_reward_already_unlocked_before(self):
        self.mock_points_repo.find_by_user_id.side_effect = [
            MagicMock(available_points=MagicMock(return_value=150)),
            MagicMock(available_points=MagicMock(return_value=200)),
        ]
        reward = RewardEntity(
            reward_id=1,
            title="Test",
            subtitle=None,
            emoji="🎁",
            achievement_id=1,
            required_points=100,
        )
        self.mock_reward_repo.find_all.return_value = [reward]

        def mutate():
            pass

        result = self.service.execute(user_id=1, mutate_points=mutate)
        self.assertFalse(result.new_reward_unlocked)

    def test_execute_returns_false_when_no_reward_reaches_threshold(self):
        self.mock_points_repo.find_by_user_id.side_effect = [
            MagicMock(available_points=MagicMock(return_value=50)),
            MagicMock(available_points=MagicMock(return_value=80)),
        ]
        reward = RewardEntity(
            reward_id=1,
            title="Test",
            subtitle=None,
            emoji="🎁",
            achievement_id=1,
            required_points=100,
        )
        self.mock_reward_repo.find_all.return_value = [reward]

        def mutate():
            pass

        result = self.service.execute(user_id=1, mutate_points=mutate)
        self.assertFalse(result.new_reward_unlocked)

    def test_execute_calls_mutate_points(self):
        self.mock_points_repo.find_by_user_id.return_value = MagicMock(
            available_points=MagicMock(return_value=0)
        )
        self.mock_reward_repo.find_all.return_value = []
        mutation_called = []

        def mutate():
            mutation_called.append(True)

        self.service.execute(user_id=1, mutate_points=mutate)
        self.assertEqual(len(mutation_called), 1)

    def test_execute_reraises_base_error_from_mutate_points(self):
        from src.domain.errors.bad_request_error import BadRequestError

        def raise_error():
            raise BadRequestError(code=400)

        with self.assertRaises(BadRequestError):
            self.service.execute(user_id=1, mutate_points=raise_error)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_points_repo.find_by_user_id.side_effect = RuntimeError("DB error")

        def noop():
            pass

        with self.assertRaises(InternalError):
            self.service.execute(user_id=1, mutate_points=noop)
