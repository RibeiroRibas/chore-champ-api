import unittest

from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.enums.user_role_enum import UserRoleEnum


class TestCurrentUserEntity(unittest.TestCase):
    def _admin_user(self, user_id: int = 1) -> CurrentUserEntity:
        return CurrentUserEntity(
            user_id=user_id,
            auth_id=10,
            role_id=UserRoleEnum.ADMIN.value[0],
            family_id=1,
        )

    def _collaborator_user(self, user_id: int = 2) -> CurrentUserEntity:
        return CurrentUserEntity(
            user_id=user_id,
            auth_id=20,
            role_id=UserRoleEnum.COLLABORATOR.value[0],
            family_id=1,
        )

    # is_admin
    def test_is_admin_returns_true_for_admin(self):
        user = self._admin_user()
        self.assertTrue(user.is_admin())

    def test_is_admin_returns_false_for_collaborator(self):
        user = self._collaborator_user()
        self.assertFalse(user.is_admin())

    # validate_chore_create_assignees
    def test_validate_chore_create_assignees_admin_succeeds_with_empty_list(self):
        user = self._admin_user()
        user.validate_chore_create_assignees([])

    def test_validate_chore_create_assignees_admin_succeeds_with_other_users(self):
        user = self._admin_user(user_id=1)
        user.validate_chore_create_assignees([99, 1])

    def test_validate_chore_create_assignees_collaborator_succeeds_when_assigning_to_self(self):
        user = self._collaborator_user(user_id=2)
        user.validate_chore_create_assignees([2])

    def test_validate_chore_create_assignees_collaborator_raises_when_empty(self):
        user = self._collaborator_user(user_id=2)
        with self.assertRaises(BadRequestError):
            user.validate_chore_create_assignees([])

    def test_validate_chore_create_assignees_collaborator_raises_when_assigning_to_other(self):
        user = self._collaborator_user(user_id=2)
        with self.assertRaises(BadRequestError):
            user.validate_chore_create_assignees([99])

    def test_validate_chore_create_assignees_collaborator_raises_when_self_and_other(self):
        user = self._collaborator_user(user_id=2)
        with self.assertRaises(BadRequestError):
            user.validate_chore_create_assignees([2, 99])
