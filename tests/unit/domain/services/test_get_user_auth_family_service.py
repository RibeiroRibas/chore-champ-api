import unittest
from unittest.mock import MagicMock

from src.domain.schemas.entity.user_auth_family_entity import UserAuthFamilyEntity
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.domain.services.get_user_auth_family_service import GetUserAuthFamilyService


class TestGetUserAuthFamilyService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = GetUserAuthFamilyService(user_repository=self.mock_repo)

    def test_execute_returns_entity_when_found_and_family_id_matches(self):
        entity = MagicMock(spec=UserAuthFamilyEntity)
        entity.family = MagicMock()
        entity.family.id = 2
        self.mock_repo.find_by_id_with_auth_and_family.return_value = entity
        result = self.service.execute(user_id=1, family_id=2)
        self.assertEqual(result, entity)
        self.mock_repo.find_by_id_with_auth_and_family.assert_called_once_with(1)

    def test_execute_raises_not_found_when_entity_is_none(self):
        self.mock_repo.find_by_id_with_auth_and_family.return_value = None
        with self.assertRaises(NotFoundError):
            self.service.execute(user_id=999, family_id=2)

    def test_execute_raises_not_found_when_family_id_does_not_match(self):
        entity = MagicMock(spec=UserAuthFamilyEntity)
        entity.family = MagicMock()
        entity.family.id = 5
        self.mock_repo.find_by_id_with_auth_and_family.return_value = entity
        with self.assertRaises(NotFoundError):
            self.service.execute(user_id=1, family_id=2)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError
        self.mock_repo.find_by_id_with_auth_and_family.side_effect = BadRequestError(code=400)
        with self.assertRaises(BadRequestError):
            self.service.execute(user_id=1, family_id=2)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_repo.find_by_id_with_auth_and_family.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.service.execute(user_id=1, family_id=2)
