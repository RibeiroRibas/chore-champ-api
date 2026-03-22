import unittest
from unittest.mock import MagicMock

from src.domain.schemas.entity.chore_entity import ChoreEntity
from src.domain.schemas.entity.chore_user_entity import ChoreUserEntity
from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.domain.errors.internal_error import InternalError
from src.application.usecases.chores.delete_chore_use_case import DeleteChoreUseCase


class TestDeleteChoreUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_get_chore_user = MagicMock()
        self.use_case = DeleteChoreUseCase(
            chore_repository=self.mock_repo,
            get_chore_user_service=self.mock_get_chore_user,
        )

    def _current_user(self, user_id=1, family_id=2, role_id=1):
        return CurrentUserEntity(
            user_id=user_id,
            auth_id=10,
            role_id=role_id,
            family_id=family_id,
        )

    def test_execute_deletes_chore_when_validation_passes(self):
        chore = ChoreEntity(
            chore_id=1,
            family_id=2,
            title="Tarefa",
            emoji="🧹",
            points=5,
            assigned_to_user_id=None,
            created_by_user_id=1,
            completed=False,
        )
        chore_user = ChoreUserEntity(user_entity=None, chore=chore)
        self.mock_get_chore_user.execute.return_value = chore_user
        current_user = self._current_user(user_id=1, family_id=2)
        self.use_case.execute(chore_id=1, current_user=current_user)
        self.mock_repo.delete_by_id.assert_called_once_with(1, 2)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.not_found_error import NotFoundError

        self.mock_get_chore_user.execute.side_effect = NotFoundError(code=404)
        with self.assertRaises(NotFoundError):
            self.use_case.execute(
                chore_id=1,
                current_user=self._current_user(),
            )

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_get_chore_user.execute.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.use_case.execute(
                chore_id=1,
                current_user=self._current_user(),
            )
