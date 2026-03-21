import unittest
from unittest.mock import MagicMock

from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.errors.not_found_error import NotFoundError
from src.domain.services.current_user_service import get_current_user_by_auth_id


class TestCurrentUserService(unittest.TestCase):
    def test_returns_user_when_found(self):
        mock_repo = MagicMock()
        expected = CurrentUserEntity(
            user_id=1,
            auth_id=10,
            role_id=1,
            family_id=2,
        )
        mock_repo.find_current_user_by_auth_id.return_value = expected
        result = get_current_user_by_auth_id(auth_id=10, user_repository=mock_repo)
        self.assertEqual(result, expected)
        mock_repo.find_current_user_by_auth_id.assert_called_once_with(10)

    def test_raises_not_found_when_user_is_none(self):
        mock_repo = MagicMock()
        mock_repo.find_current_user_by_auth_id.return_value = None
        with self.assertRaises(NotFoundError):
            get_current_user_by_auth_id(auth_id=999, user_repository=mock_repo)
