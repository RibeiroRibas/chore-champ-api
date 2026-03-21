import unittest
from unittest.mock import MagicMock

from src.domain.entities.day_of_week_entity import DayOfWeekEntity
from src.domain.errors.internal_error import InternalError
from src.application.usecases.days_of_week.list_days_of_week_use_case import (
    ListDaysOfWeekUseCase,
)


class TestListDaysOfWeekUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.use_case = ListDaysOfWeekUseCase(
            day_of_week_repository=self.mock_repo
        )

    def test_execute_returns_empty_list_when_no_entities(self):
        self.mock_repo.find_all.return_value = []
        result = self.use_case.execute()
        self.assertEqual(result, [])
        self.mock_repo.find_all.assert_called_once()

    def test_execute_returns_responses_for_each_entity(self):
        entities = [
            DayOfWeekEntity(id=1, name="Segunda"),
            DayOfWeekEntity(id=2, name="Terça"),
        ]
        self.mock_repo.find_all.return_value = entities
        result = self.use_case.execute()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].name, "Segunda")
        self.assertEqual(result[1].id, 2)
        self.assertEqual(result[1].name, "Terça")

    def test_execute_raises_internal_error_on_exception(self):
        self.mock_repo.find_all.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.use_case.execute()
