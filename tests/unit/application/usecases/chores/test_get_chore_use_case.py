import unittest
from unittest.mock import MagicMock

from src.domain.entities.chore_entity import ChoreEntity
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.application.usecases.chores.get_chore_use_case import GetChoreUseCase


class TestGetChoreUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.use_case = GetChoreUseCase(chore_repository=self.mock_repo)

    def test_execute_returns_response_when_chore_found(self):
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
        result = self.use_case.execute(chore_id=1, family_id=2)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.title, "Tarefa")
        self.mock_repo.find_by_id.assert_called_once_with(1, 2)

    def test_execute_raises_not_found_when_chore_is_none(self):
        self.mock_repo.find_by_id.return_value = None
        with self.assertRaises(NotFoundError):
            self.use_case.execute(chore_id=999, family_id=2)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError

        self.mock_repo.find_by_id.side_effect = BadRequestError(code=400)
        with self.assertRaises(BadRequestError):
            self.use_case.execute(chore_id=1, family_id=2)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_repo.find_by_id.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.use_case.execute(chore_id=1, family_id=2)
