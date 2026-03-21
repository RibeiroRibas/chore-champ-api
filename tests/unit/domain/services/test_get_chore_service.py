import unittest
from unittest.mock import MagicMock

from src.domain.entities.chore_entity import ChoreEntity
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.domain.services.get_chore_service import GetChoreService


class TestGetChoreService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = GetChoreService(chore_repository=self.mock_repo)

    def test_execute_returns_entity_when_found(self):
        chore = ChoreEntity(
            chore_id=1,
            family_id=2,
            title="Tarefa",
            emoji="🧹",
            points=10,
            assigned_to_user_id=3,
            created_by_user_id=1,
            completed=False,
        )
        self.mock_repo.find_by_id.return_value = chore
        result = self.service.execute(chore_id=1, family_id=2)
        self.assertEqual(result, chore)
        self.mock_repo.find_by_id.assert_called_once_with(chore_id=1, family_id=2)

    def test_execute_raises_not_found_when_entity_is_none(self):
        self.mock_repo.find_by_id.return_value = None
        with self.assertRaises(NotFoundError):
            self.service.execute(chore_id=999, family_id=2)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError
        self.mock_repo.find_by_id.side_effect = BadRequestError(code=400)
        with self.assertRaises(BadRequestError):
            self.service.execute(chore_id=1, family_id=2)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_repo.find_by_id.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.service.execute(chore_id=1, family_id=2)
