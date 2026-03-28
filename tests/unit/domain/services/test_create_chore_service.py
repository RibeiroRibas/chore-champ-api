import unittest
from unittest.mock import MagicMock

from src.domain.schemas.dto.chores.create_chore_dto import CreateChoreDTO
from src.domain.schemas.entity.chore_entity import ChoreEntity
from src.domain.schemas.entity.new_reward_unlock_check_entity import NewRewardUnlockCheckEntity
from src.domain.errors.internal_error import InternalError
from src.domain.services.create_chore_service import CreateChoreService


class TestCreateChoreService(unittest.TestCase):
    def setUp(self):
        self.mock_chore_repo = MagicMock()
        self.mock_recurring_service = MagicMock()
        self.mock_save_points = MagicMock()
        self.mock_detect = MagicMock()
        self.service = CreateChoreService(
            chore_repository=self.mock_chore_repo,
            recurring_chore_service=self.mock_recurring_service,
            save_user_points_service=self.mock_save_points,
            detect_new_reward_unlocked_service=self.mock_detect,
        )

    def _dto(
        self,
        *,
        assigned_to_user_id=None,
        completed=False,
        is_recurring=False,
        recurrence_day_ids=None,
    ) -> CreateChoreDTO:
        return CreateChoreDTO(
            family_id=1,
            title="T",
            emoji="🧹",
            points=10,
            created_by_user_id=1,
            assigned_to_user_id=assigned_to_user_id,
            completed=completed,
            is_recurring=is_recurring,
            recurrence_day_ids=recurrence_day_ids,
        )

    def _entity(self) -> ChoreEntity:
        return ChoreEntity(
            chore_id=99,
            family_id=1,
            title="T",
            emoji="🧹",
            points=10,
            assigned_to_user_id=None,
            created_by_user_id=1,
            completed=False,
        )

    def test_execute_inserts_only_when_not_recurring_and_not_completed(self):
        dto = self._dto()
        self.mock_chore_repo.insert.return_value = self._entity()
        new_reward_unlocked = self.service.execute(dto)
        self.assertFalse(new_reward_unlocked)
        self.mock_chore_repo.insert.assert_called_once()
        self.mock_recurring_service.execute.assert_not_called()
        self.mock_detect.execute.assert_not_called()

    def test_execute_inserts_recurring_when_recurring(self):
        dto = self._dto(is_recurring=True, recurrence_day_ids=[1, 2])
        self.mock_chore_repo.insert.return_value = self._entity()
        new_reward_unlocked = self.service.execute(dto)
        self.assertFalse(new_reward_unlocked)
        self.mock_recurring_service.execute.assert_called_once()
        passed = self.mock_recurring_service.execute.call_args.kwargs["dto"]
        self.assertEqual(passed.chore_id, 99)
        self.assertEqual(passed.day_of_the_week_ids, [1, 2])
        self.assertTrue(passed.is_recurring)

    def test_execute_detects_reward_when_completed_with_assignee(self):
        dto = self._dto(assigned_to_user_id=1, completed=True)
        self.mock_chore_repo.insert.return_value = self._entity()

        def detect_side_effect(user_id, mutate_points):
            mutate_points()
            return NewRewardUnlockCheckEntity(
                available_points_before=0,
                available_points_after=10,
                new_reward_unlocked=True,
            )

        self.mock_detect.execute.side_effect = detect_side_effect
        new_reward_unlocked = self.service.execute(dto)
        self.assertTrue(new_reward_unlocked)
        self.mock_detect.execute.assert_called_once()
        self.mock_save_points.execute.assert_called_once()

    def test_execute_returns_false_when_completed_but_unassigned(self):
        dto = self._dto(assigned_to_user_id=None, completed=True)
        self.mock_chore_repo.insert.return_value = self._entity()
        new_reward_unlocked = self.service.execute(dto)
        self.assertFalse(new_reward_unlocked)
        self.mock_detect.execute.assert_not_called()

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        dto = self._dto()
        self.mock_chore_repo.insert.side_effect = RuntimeError("fail")
        with self.assertRaises(InternalError):
            self.service.execute(dto)
