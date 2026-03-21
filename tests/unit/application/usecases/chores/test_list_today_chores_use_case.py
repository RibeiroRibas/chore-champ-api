import unittest
from unittest.mock import MagicMock

from src.domain.entities.chore_entity import ChoreEntity
from src.domain.errors.internal_error import InternalError
from src.application.usecases.chores.list_today_chores_use_case import (
    ListTodayChoresUseCase,
)


class TestListTodayChoresUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_service = MagicMock()
        self.use_case = ListTodayChoresUseCase(
            list_today_chore_entities_service=self.mock_service
        )

    def test_execute_returns_empty_list_when_no_chores(self):
        self.mock_service.execute.return_value = []
        result = self.use_case.execute(family_id=1)
        self.assertEqual(result, [])
        self.mock_service.execute.assert_called_once_with(1)

    def test_execute_returns_responses_for_each_chore(self):
        chores = [
            ChoreEntity(
                chore_id=1,
                family_id=1,
                title="Tarefa 1",
                emoji="🧹",
                points=5,
                assigned_to_user_id=None,
                created_by_user_id=1,
                completed=False,
            ),
        ]
        self.mock_service.execute.return_value = chores
        result = self.use_case.execute(family_id=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].title, "Tarefa 1")

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError

        self.mock_service.execute.side_effect = BadRequestError(code=400)
        with self.assertRaises(BadRequestError):
            self.use_case.execute(family_id=1)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_service.execute.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.use_case.execute(family_id=1)
