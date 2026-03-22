import unittest
from unittest.mock import MagicMock

from src.domain.schemas.entity.chore_user_entity import ChoreUserEntity
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.domain.services.get_chore_user_service import GetChoreUSerService


class TestGetChoreUserService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = GetChoreUSerService(chore_repository=self.mock_repo)

    def test_execute_returns_entity_when_found(self):
        entity = MagicMock(spec=ChoreUserEntity)
        self.mock_repo.find_by_id_with_user.return_value = entity
        result = self.service.execute(chore_id=1, family_id=2)
        self.assertEqual(result, entity)
        self.mock_repo.find_by_id_with_user.assert_called_once_with(chore_id=1, family_id=2)

    def test_execute_raises_not_found_when_entity_is_none(self):
        self.mock_repo.find_by_id_with_user.return_value = None
        with self.assertRaises(NotFoundError):
            self.service.execute(chore_id=999, family_id=2)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError
        self.mock_repo.find_by_id_with_user.side_effect = BadRequestError(code=400)
        with self.assertRaises(BadRequestError):
            self.service.execute(chore_id=1, family_id=2)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_repo.find_by_id_with_user.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.service.execute(chore_id=1, family_id=2)
