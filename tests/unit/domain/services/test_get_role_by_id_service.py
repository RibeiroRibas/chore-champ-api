import unittest
from unittest.mock import MagicMock

from src.domain.schemas.entity.role_entity import RoleEntity
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.domain.services.get_role_by_id_service import GetRoleByIdService


class TestGetRoleByIdService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = GetRoleByIdService(role_repository=self.mock_repo)

    def test_execute_returns_role_when_found(self):
        role = RoleEntity(role_id=1, name="Admin")
        self.mock_repo.find_by_id.return_value = role
        result = self.service.execute(role_id=1)
        self.assertEqual(result, role)
        self.mock_repo.find_by_id.assert_called_once_with(1)

    def test_execute_raises_not_found_when_role_is_none(self):
        self.mock_repo.find_by_id.return_value = None
        with self.assertRaises(NotFoundError):
            self.service.execute(role_id=999)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError
        self.mock_repo.find_by_id.side_effect = BadRequestError(code=400)
        with self.assertRaises(BadRequestError):
            self.service.execute(role_id=1)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_repo.find_by_id.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.service.execute(role_id=1)
