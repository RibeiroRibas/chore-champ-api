import unittest
from unittest.mock import MagicMock, patch

from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.recurring_chore_entity import RecurringChoreEntity
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
        self.mock_chore_repo.find_today_chore_by_family_id.return_value = []
        self.mock_recurring_repo.find_by_parent_chore_id_and_day.return_value = []
        result = self.service.execute(family_id=1)
        self.assertEqual(result, [])

    def test_execute_returns_non_recurring_chores_only(self):
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
        self.mock_chore_repo.find_today_chore_by_family_id.return_value = [chore]
        self.mock_recurring_repo.find_by_parent_chore_id_and_day.return_value = []
        result = self.service.execute(family_id=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], chore)

    def test_execute_includes_recurring_chores_matching_today(self):
        from src.domain.entities.day_of_week_entity import DayOfWeekEntity

        recurring_chore = ChoreEntity(
            chore_id=1,
            family_id=1,
            title="Recurring",
            emoji="🔄",
            points=3,
            assigned_to_user_id=None,
            created_by_user_id=1,
            completed=False,
            is_recurring=True,
        )
        rec_entity = RecurringChoreEntity(
            chore_id=2,
            day_of_week=DayOfWeekEntity(6, "Sábado"),
            parent_chore_id=1,
        )
        child_chore = ChoreEntity(
            chore_id=2,
            family_id=1,
            title="Child",
            emoji="🔄",
            points=3,
            assigned_to_user_id=None,
            created_by_user_id=1,
            completed=False,
            is_recurring=True,
        )
        self.mock_chore_repo.find_today_chore_by_family_id.return_value = [
            recurring_chore
        ]
        with patch(
            "src.domain.services.list_today_chore_entities_service.datetime"
        ) as mock_dt:
            mock_dt.now.return_value.weekday.return_value = 5
            self.mock_recurring_repo.find_by_parent_chore_id_and_day.return_value = [
                rec_entity
            ]
            self.mock_chore_repo.find_by_id.return_value = child_chore
            result = self.service.execute(family_id=1)
            self.assertGreater(len(result), 0)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError

        self.mock_chore_repo.find_today_chore_by_family_id.side_effect = (
            BadRequestError(code=400)
        )
        with self.assertRaises(BadRequestError):
            self.service.execute(family_id=1)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_chore_repo.find_today_chore_by_family_id.side_effect = RuntimeError(
            "DB error"
        )
        with self.assertRaises(InternalError):
            self.service.execute(family_id=1)
