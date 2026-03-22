import unittest

from src.domain.schemas.entity.reward_entity import RewardEntity
from src.domain.errors.bad_request_error import BadRequestError


class TestRewardEntity(unittest.TestCase):
    def _reward(
        self,
        reward_id: int = 1,
        required_points: int | None = 100,
    ) -> RewardEntity:
        return RewardEntity(
            reward_id=reward_id,
            title="Pizza",
            subtitle="Noite de pizza",
            emoji="🍕",
            achievement_id=1,
            required_points=required_points,
        )

    # is_unlocked
    def test_is_unlocked_returns_true_when_points_greater_or_equal(self):
        reward = self._reward(required_points=100)
        self.assertTrue(reward.is_unlocked(100))
        self.assertTrue(reward.is_unlocked(150))

    def test_is_unlocked_returns_false_when_points_less(self):
        reward = self._reward(required_points=100)
        self.assertFalse(reward.is_unlocked(99))

    def test_is_unlocked_returns_false_when_required_points_none(self):
        reward = self._reward(required_points=None)
        self.assertFalse(reward.is_unlocked(1000))

    # validate_can_claim
    def test_validate_can_claim_succeeds_when_unlocked(self):
        reward = self._reward(required_points=100)
        reward.validate_can_claim(100)
        reward.validate_can_claim(150)

    def test_validate_can_claim_raises_when_not_unlocked(self):
        reward = self._reward(required_points=100)
        with self.assertRaises(BadRequestError):
            reward.validate_can_claim(99)

    def test_validate_can_claim_raises_when_required_points_none(self):
        reward = self._reward(required_points=None)
        with self.assertRaises(BadRequestError):
            reward.validate_can_claim(1000)
