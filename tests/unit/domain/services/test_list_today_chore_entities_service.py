import unittest
from unittest.mock import MagicMock, patch

from src.domain.schemas.entity.chore_entity import ChoreEntity
from src.domain.errors.internal_error import InternalError
from src.domain.services.list_today_chore_entities_service import (
    ListTodayChoreEntitiesService,
)


class TestListTodayChoreEntitiesService(unittest.TestCase):
    def setUp(self):
        self.mock_chore_repo = MagicMock()
        self.mock_recurring_repo = MagicMock()
        self.service = ListTodayChoreEntitiesService(
            chore_repository=self.mock_chore_repo,
            recurring_chore_repository=self.mock_recurring_repo,
        )

    def test_execute_returns_empty_list_when_no_chores(self):
        self.mock_chore_repo.find_today_chores.return_value = []
        with patch(
            "src.domain.services.list_today_chore_entities_service.datetime"
        ) as mock_dt:
            mock_dt.now.return_value.weekday.return_value = 0
            result = self.service.execute(family_id=1)
        self.assertEqual(result, [])
        self.mock_chore_repo.find_today_chores.assert_called_once_with(
            1, 1, assigned_to_user_id=None,
        )

    def test_execute_returns_chores_from_find_today_chores(self):
        chore = ChoreEntity(
            chore_id=1,
            family_id=1,
            title="Tarefa",
            emoji="🧹",
            points=5,
            assigned_to_user_id=None,
            created_by_user_id=1,
            completed=False,
            is_recurring=False,
        )
        self.mock_chore_repo.find_today_chores.return_value = [chore]
        with patch(
            "src.domain.services.list_today_chore_entities_service.datetime"
        ) as mock_dt:
            mock_dt.now.return_value.weekday.return_value = 2
            result = self.service.execute(family_id=42)
        self.assertEqual(result, [chore])
        self.mock_chore_repo.find_today_chores.assert_called_once_with(
            42, 3, assigned_to_user_id=None,
        )

    def test_execute_passes_assigned_to_user_id_to_repository(self):
        self.mock_chore_repo.find_today_chores.return_value = []
        with patch(
            "src.domain.services.list_today_chore_entities_service.datetime"
        ) as mock_dt:
            mock_dt.now.return_value.weekday.return_value = 0
            self.service.execute(family_id=1, assigned_to_user_id=9)
        self.mock_chore_repo.find_today_chores.assert_called_once_with(
            1, 1, assigned_to_user_id=9,
        )

    def test_execute_passes_weekday_plus_one_to_repository(self):
        self.mock_chore_repo.find_today_chores.return_value = []
        with patch(
            "src.domain.services.list_today_chore_entities_service.datetime"
        ) as mock_dt:
            mock_dt.now.return_value.weekday.return_value = 6
            self.service.execute(family_id=1)
        self.mock_chore_repo.find_today_chores.assert_called_once_with(
            1, 7, assigned_to_user_id=None,
        )

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError

        self.mock_chore_repo.find_today_chores.side_effect = BadRequestError(code=400)
        with self.assertRaises(BadRequestError):
            self.service.execute(family_id=1)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_chore_repo.find_today_chores.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.service.execute(family_id=1)
