import unittest
from unittest.mock import MagicMock

from src.domain.entities.chore_entity import ChoreEntity
from src.domain.errors.internal_error import InternalError
from src.domain.errors.not_found_error import NotFoundError
from src.domain.schemas.recurring_chore_dto import RecurringChoreDTO
from src.domain.services.recurring_chore_service import RecurringChoreService


class TestRecurringChoreService(unittest.TestCase):
    def setUp(self):
        self.mock_chore_repo = MagicMock()
        self.mock_recurring_repo = MagicMock()
        self.service = RecurringChoreService(
            chore_repository=self.mock_chore_repo,
            recurring_chore_repository=self.mock_recurring_repo,
        )

    def test_execute_deletes_and_inserts_when_chore_not_completed(self):
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=False,
            is_recurring=True,
            day_of_the_week_ids=[1, 2, 3],
        )
        self.service.execute(dto=dto)
        self.mock_recurring_repo.delete_by_chore_id.assert_called_once_with(
            10, 1, commit=False
        )
        self.mock_recurring_repo.insert_recurring_chores.assert_called_once_with(
            dto=dto
        )
        self.mock_chore_repo.find_by_id.assert_not_called()

    def test_execute_raises_not_found_when_chore_not_found_and_completed(self):
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=True,
        )
        self.mock_chore_repo.find_by_id.return_value = None
        with self.assertRaises(NotFoundError):
            self.service.execute(dto=dto)

    def test_execute_deletes_only_when_completed_and_not_recurring(self):
        chore = ChoreEntity(
            chore_id=10,
            family_id=1,
            title="Tarefa",
            emoji="🧹",
            points=5,
            assigned_to_user_id=None,
            created_by_user_id=1,
            completed=True,
            is_recurring=False,
        )
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=True,
            is_recurring=False,
        )
        self.mock_chore_repo.find_by_id.return_value = chore
        self.service.execute(dto=dto)
        self.mock_recurring_repo.delete_by_chore_id.assert_called_once_with(10, 1)
        self.mock_chore_repo.insert_copy.assert_not_called()

    def test_execute_inserts_copy_and_recurring_when_chore_is_recurring(self):
        chore = ChoreEntity(
            chore_id=10,
            family_id=1,
            title="Tarefa",
            emoji="🧹",
            points=5,
            assigned_to_user_id=None,
            created_by_user_id=1,
            completed=True,
            is_recurring=True,
        )
        copy_chore = ChoreEntity(
            chore_id=20,
            family_id=1,
            title="Tarefa",
            emoji="🧹",
            points=5,
            assigned_to_user_id=None,
            created_by_user_id=1,
            completed=False,
            is_recurring=True,
        )
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=True,
            is_recurring=True,
            day_of_the_week_ids=[1, 2],
        )
        self.mock_chore_repo.find_by_id.return_value = chore
        self.mock_chore_repo.insert_copy.return_value = copy_chore
        self.service.execute(dto=dto)
        self.mock_chore_repo.insert_copy.assert_called_once_with(
            source_entity=chore, commit=False
        )
        self.mock_recurring_repo.insert_recurring_chores.assert_called_once()
        call_dto = self.mock_recurring_repo.insert_recurring_chores.call_args.kwargs[
            "dto"
        ]
        self.assertEqual(call_dto.chore_id, 20)
        self.assertEqual(call_dto.parent_chore_id, 10)
        self.mock_recurring_repo.delete_by_chore_id.assert_called_once_with(10, 1)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError

        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=False,
        )
        self.mock_recurring_repo.delete_by_chore_id.side_effect = BadRequestError(
            code=400
        )
        with self.assertRaises(BadRequestError):
            self.service.execute(dto=dto)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        dto = RecurringChoreDTO(
            family_id=1,
            chore_id=10,
            is_chore_completed=False,
        )
        self.mock_recurring_repo.delete_by_chore_id.side_effect = RuntimeError(
            "DB error"
        )
        with self.assertRaises(InternalError):
            self.service.execute(dto=dto)
