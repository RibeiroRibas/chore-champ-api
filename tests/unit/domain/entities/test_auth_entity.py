import unittest
from unittest.mock import patch

from src.domain.entities.auth_entity import AuthEntity


class TestAuthEntity(unittest.TestCase):
    def _auth(self, password: str = "hashed") -> AuthEntity:
        return AuthEntity(id=1, username="user@test.com", password=password)

    @patch("src.domain.entities.auth_entity.verify_password")
    def test_is_password_equals_returns_true_when_match(self, mock_verify):
        mock_verify.return_value = True
        auth = self._auth(password="hashed")
        self.assertTrue(auth.is_password_equals("plain"))
        mock_verify.assert_called_once_with("plain", "hashed")

    @patch("src.domain.entities.auth_entity.verify_password")
    def test_is_password_equals_returns_false_when_no_match(self, mock_verify):
        mock_verify.return_value = False
        auth = self._auth(password="hashed")
        self.assertFalse(auth.is_password_equals("wrong"))
        mock_verify.assert_called_once_with("wrong", "hashed")
