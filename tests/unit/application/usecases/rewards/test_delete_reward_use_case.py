import unittest
from unittest.mock import MagicMock

from src.domain.errors.internal_error import InternalError
from src.application.usecases.rewards.delete_reward_use_case import DeleteRewardUseCase


class TestDeleteRewardUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.use_case = DeleteRewardUseCase(reward_repository=self.mock_repo)

    def test_execute_calls_repository_delete(self):
        self.use_case.execute(reward_id=1)
        self.mock_repo.delete_by_id.assert_called_once_with(reward_id=1)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.not_found_error import NotFoundError

        self.mock_repo.delete_by_id.side_effect = NotFoundError(code=404)
        with self.assertRaises(NotFoundError):
            self.use_case.execute(reward_id=1)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_repo.delete_by_id.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.use_case.execute(reward_id=1)
