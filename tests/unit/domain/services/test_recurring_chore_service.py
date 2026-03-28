import unittest
from unittest.mock import MagicMock

from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.internal_error import InternalError
from src.domain.schemas.dto.chores.recurring_chore_dto import RecurringChoreDTO
from src.domain.schemas.entity.day_of_week_entity import DayOfWeekEntity
from src.domain.schemas.entity.recurring_chore_entity import RecurringChoreEntity
from src.domain.services.recurring_chore_service import RecurringChoreService


class TestRecurringChoreService(unittest.TestCase):
    def setUp(self):
        self.mock_recurring_repo = MagicMock()
        self.service = RecurringChoreService(
            recurring_chore_repository=self.mock_recurring_repo,
        )

    def test_execute_deletes_when_should_delete_empty_days(self):
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=False,
            is_recurring=True,
            day_of_the_week_ids=[],
        )
        self.service.execute(dto=dto)
        self.mock_recurring_repo.delete_by_chore_id.assert_called_once_with(10, 1, True)
        self.mock_recurring_repo.find_by_chore_id.assert_not_called()

    def test_execute_inserts_when_no_rows_in_db(self):
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=False,
            is_recurring=True,
            day_of_the_week_ids=[1, 2, 3],
        )
        self.mock_recurring_repo.find_by_chore_id.return_value = None
        self.service.execute(dto=dto)
        self.mock_recurring_repo.find_by_chore_id.assert_called_once_with(10, 1)
        self.mock_recurring_repo.insert_recurring_chores.assert_called_once_with(
            dto=dto, commit=True
        )

    def test_execute_inserts_when_empty_list_from_db(self):
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=False,
            is_recurring=True,
            day_of_the_week_ids=[1],
        )
        self.mock_recurring_repo.find_by_chore_id.return_value = []
        self.service.execute(dto=dto)
        self.mock_recurring_repo.insert_recurring_chores.assert_called_once_with(
            dto=dto, commit=True
        )

    def test_execute_raises_bad_request_when_completed_not_today(self):
        """Hoje é sempre weekday()+1 em 1..7; [9] nunca coincide."""
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=True,
            is_recurring=True,
            day_of_the_week_ids=[9],
        )
        with self.assertRaises(BadRequestError):
            self.service.execute(dto=dto)

    def test_execute_processes_existing_rows_without_insert_when_no_changes(self):
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=False,
            is_recurring=True,
            day_of_the_week_ids=[1],
        )
        existing = [
            RecurringChoreEntity(
                chore_id=10,
                day_of_week=DayOfWeekEntity(id=1, name="Seg"),
                completed_at=None,
            )
        ]
        self.mock_recurring_repo.find_by_chore_id.return_value = existing
        self.service.execute(dto=dto)
        self.mock_recurring_repo.insert_recurring_chores.assert_not_called()
        self.mock_recurring_repo.delete_by_chore_id.assert_not_called()

    def test_execute_reraises_base_error(self):
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=False,
            is_recurring=True,
            day_of_the_week_ids=[1],
        )
        self.mock_recurring_repo.find_by_chore_id.return_value = None
        self.mock_recurring_repo.insert_recurring_chores.side_effect = BadRequestError(
            code=400
        )
        with self.assertRaises(BadRequestError):
            self.service.execute(dto=dto)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=False,
            is_recurring=True,
            day_of_the_week_ids=[1],
        )
        self.mock_recurring_repo.find_by_chore_id.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.service.execute(dto=dto)
