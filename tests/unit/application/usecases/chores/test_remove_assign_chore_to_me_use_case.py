import unittest
from unittest.mock import MagicMock

from src.domain.schemas.entity.chore_entity import ChoreEntity
from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.domain.errors.internal_error import InternalError
from src.application.usecases.chores.remove_assign_chore_to_me_use_case import (
    RemoveAssignChoreToMeUseCase,
)


class TestRemoveAssignChoreToMeUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_get_chore = MagicMock()
        self.use_case = RemoveAssignChoreToMeUseCase(
            chore_repository=self.mock_repo,
            get_chore_service=self.mock_get_chore,
        )

    def _current_user(self, user_id=1, family_id=2):
        return CurrentUserEntity(
            user_id=user_id,
            auth_id=10,
            role_id=1,
            family_id=family_id,
        )

    def test_execute_updates_chore_with_none_assignee(self):
        chore = ChoreEntity(
            chore_id=1,
            family_id=2,
            title="Tarefa",
            emoji="🧹",
            points=5,
            assigned_to_user_id=1,
            created_by_user_id=1,
            completed=False,
        )
        self.mock_get_chore.execute.return_value = chore
        current_user = self._current_user(user_id=1, family_id=2)
        self.use_case.execute(chore_id=1, current_user=current_user)
        self.mock_repo.update.assert_called_once()
        call_kwargs = self.mock_repo.update.call_args.kwargs
        self.assertIsNone(call_kwargs["update_chore_dto"].assigned_to_user_id)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.not_found_error import NotFoundError

        self.mock_get_chore.execute.side_effect = NotFoundError(code=404)
        with self.assertRaises(NotFoundError):
            self.use_case.execute(
                chore_id=1,
                current_user=self._current_user(),
            )

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_get_chore.execute.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.use_case.execute(
                chore_id=1,
                current_user=self._current_user(),
            )
