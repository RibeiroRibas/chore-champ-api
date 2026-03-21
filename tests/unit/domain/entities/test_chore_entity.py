import unittest

from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.unauthorized_error import UnauthorizedError
from src.domain.enums.user_role_enum import UserRoleEnum


class TestChoreEntity(unittest.TestCase):
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

    def _chore(
        self,
        chore_id: int = 1,
        assigned_to_user_id: int | None = None,
        created_by_user_id: int = 1,
        completed: bool = False,
    ) -> ChoreEntity:
        return ChoreEntity(
            chore_id=chore_id,
            family_id=1,
            title="Lavar louça",
            emoji="🧽",
            points=10,
            assigned_to_user_id=assigned_to_user_id,
            created_by_user_id=created_by_user_id,
            completed=completed,
        )

    # validate_can_update_or_delete
    def test_validate_can_update_or_delete_does_not_raise_when_not_completed(self):
        chore = self._chore(completed=False)
        chore.validate_can_update_or_delete()

    def test_validate_can_update_or_delete_raises_when_completed(self):
        chore = self._chore(completed=True)
        with self.assertRaises(BadRequestError):
            chore.validate_can_update_or_delete()

    # validate_has_update_permission
    def test_validate_has_update_permission_admin_succeeds(self):
        chore = self._chore(created_by_user_id=99)
        admin = self._admin_user(user_id=1)
        chore.validate_has_update_permission(admin)

    def test_validate_has_update_permission_creator_succeeds(self):
        chore = self._chore(created_by_user_id=2)
        collaborator = self._collaborator_user(user_id=2)
        chore.validate_has_update_permission(collaborator)

    def test_validate_has_update_permission_non_creator_non_admin_raises(self):
        chore = self._chore(created_by_user_id=1)
        collaborator = self._collaborator_user(user_id=2)
        with self.assertRaises(UnauthorizedError):
            chore.validate_has_update_permission(collaborator)

    # validate_has_delete_permission
    def test_validate_has_delete_permission_admin_succeeds(self):
        chore = self._chore(created_by_user_id=99)
        admin = self._admin_user(user_id=1)
        chore.validate_has_delete_permission(admin)

    def test_validate_has_delete_permission_creator_succeeds(self):
        chore = self._chore(created_by_user_id=2)
        collaborator = self._collaborator_user(user_id=2)
        chore.validate_has_delete_permission(collaborator)

    def test_validate_has_delete_permission_non_creator_non_admin_raises(self):
        chore = self._chore(created_by_user_id=1)
        collaborator = self._collaborator_user(user_id=2)
        with self.assertRaises(UnauthorizedError):
            chore.validate_has_delete_permission(collaborator)

    # validate_can_assign_to_current_user
    def test_validate_can_assign_raises_when_chore_completed(self):
        chore = self._chore(completed=True, assigned_to_user_id=None)
        admin = self._admin_user()
        with self.assertRaises(BadRequestError):
            chore.validate_can_assign_to_current_user(admin)

    def test_validate_can_assign_admin_succeeds_even_when_already_assigned(self):
        chore = self._chore(assigned_to_user_id=2, completed=False)
        admin = self._admin_user()
        chore.validate_can_assign_to_current_user(admin)

    def test_validate_can_assign_collaborator_succeeds_when_unassigned(self):
        chore = self._chore(assigned_to_user_id=None, completed=False)
        collaborator = self._collaborator_user(user_id=2)
        chore.validate_can_assign_to_current_user(collaborator)

    def test_validate_can_assign_collaborator_raises_when_already_assigned(self):
        chore = self._chore(assigned_to_user_id=3, completed=False)
        collaborator = self._collaborator_user(user_id=2)
        with self.assertRaises(BadRequestError):
            chore.validate_can_assign_to_current_user(collaborator)

    # validate_can_remove_assignment
    def test_validate_can_remove_assignment_raises_when_completed(self):
        chore = self._chore(completed=True, assigned_to_user_id=2)
        admin = self._admin_user()
        with self.assertRaises(BadRequestError):
            chore.validate_can_remove_assignment(admin)

    def test_validate_can_remove_assignment_raises_when_not_assigned(self):
        chore = self._chore(assigned_to_user_id=None)
        admin = self._admin_user()
        with self.assertRaises(BadRequestError):
            chore.validate_can_remove_assignment(admin)

    def test_validate_can_remove_assignment_admin_succeeds(self):
        chore = self._chore(assigned_to_user_id=2)
        admin = self._admin_user()
        chore.validate_can_remove_assignment(admin)

    def test_validate_can_remove_assignment_collaborator_raises(self):
        chore = self._chore(assigned_to_user_id=2)
        collaborator = self._collaborator_user(user_id=2)
        with self.assertRaises(BadRequestError):
            chore.validate_can_remove_assignment(collaborator)

    # validate_can_complete
    def test_validate_can_complete_raises_when_already_completed(self):
        chore = self._chore(completed=True, assigned_to_user_id=2)
        admin = self._admin_user()
        with self.assertRaises(BadRequestError):
            chore.validate_can_complete(admin, [])

    def test_validate_can_complete_admin_succeeds_even_when_not_assigned(self):
        chore = self._chore(assigned_to_user_id=None, completed=False)
        admin = self._admin_user()
        chore.validate_can_complete(admin, [])

    def test_validate_can_complete_collaborator_raises_when_not_assigned(self):
        chore = self._chore(assigned_to_user_id=None)
        collaborator = self._collaborator_user(user_id=2)
        with self.assertRaises(BadRequestError):
            chore.validate_can_complete(collaborator, [chore])

    def test_validate_can_complete_collaborator_raises_when_assigned_to_other(self):
        chore = self._chore(assigned_to_user_id=3)
        collaborator = self._collaborator_user(user_id=2)
        with self.assertRaises(BadRequestError):
            chore.validate_can_complete(collaborator, [chore])

    def test_validate_can_complete_collaborator_raises_when_not_in_today_list(self):
        chore = self._chore(chore_id=1, assigned_to_user_id=2)
        other = ChoreEntity(
            chore_id=99,
            family_id=1,
            title="Other",
            emoji="📦",
            points=5,
            assigned_to_user_id=2,
            created_by_user_id=1,
            completed=False,
        )
        collaborator = self._collaborator_user(user_id=2)
        with self.assertRaises(BadRequestError):
            chore.validate_can_complete(collaborator, [other])

    def test_validate_can_complete_collaborator_succeeds_when_in_today_list(self):
        chore = self._chore(chore_id=1, assigned_to_user_id=2)
        collaborator = self._collaborator_user(user_id=2)
        chore.validate_can_complete(collaborator, [chore])

    # is_chore_in_today_list
    def test_is_chore_in_today_list_returns_true_when_present(self):
        chore = self._chore(chore_id=1)
        other = self._chore(chore_id=99)
        self.assertTrue(chore.is_chore_in_today_list([chore, other]))

    def test_is_chore_in_today_list_returns_false_when_absent(self):
        chore = self._chore(chore_id=1)
        other = self._chore(chore_id=99)
        self.assertFalse(chore.is_chore_in_today_list([other]))

    def test_is_chore_in_today_list_returns_false_when_empty(self):
        chore = self._chore(chore_id=1)
        self.assertFalse(chore.is_chore_in_today_list([]))
