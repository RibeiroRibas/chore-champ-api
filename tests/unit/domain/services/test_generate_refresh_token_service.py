import unittest
from unittest.mock import MagicMock

from src.domain.errors.internal_error import InternalError
from src.domain.services.generate_refresh_token_service import GenerateRefreshTokenService


class TestGenerateRefreshTokenService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = GenerateRefreshTokenService(
            refresh_token_repository=self.mock_repo
        )

    def test_execute_deletes_old_tokens_and_inserts_new(self):
        self.mock_repo.insert.return_value = None
        result = self.service.execute(auth_id=1)
        self.mock_repo.delete_by_auth_id.assert_called_once_with(
            auth_id=1, commit=False
        )
        self.mock_repo.insert.assert_called_once()
        call_args = self.mock_repo.insert.call_args
        self.assertEqual(call_args.kwargs["auth_id"], 1)
        self.assertIsInstance(call_args.kwargs["refresh_token"], str)
        self.assertGreater(len(call_args.kwargs["refresh_token"]), 0)
        self.assertEqual(result, call_args.kwargs["refresh_token"])

    def test_execute_returns_different_tokens_on_each_call(self):
        tokens = set()
        for _ in range(5):
            result = self.service.execute(auth_id=1)
            tokens.add(result)
        self.assertEqual(len(tokens), 5)

    def test_execute_raises_internal_error_on_exception(self):
        self.mock_repo.delete_by_auth_id.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.service.execute(auth_id=1)
