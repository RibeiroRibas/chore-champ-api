import unittest

from src.domain.schemas.entity.role_entity import RoleEntity
from src.domain.enums.user_role_enum import UserRoleEnum


class TestRoleEntity(unittest.TestCase):
    def test_get_role_returns_admin_for_admin_id(self):
        role = RoleEntity(role_id=UserRoleEnum.ADMIN.value[0], name="Administrator")
        self.assertEqual(role.get_role(), UserRoleEnum.ADMIN)

    def test_get_role_returns_collaborator_for_collaborator_id(self):
        role = RoleEntity(role_id=UserRoleEnum.COLLABORATOR.value[0], name="Colaborador")
        self.assertEqual(role.get_role(), UserRoleEnum.COLLABORATOR)

    def test_get_role_returns_collaborator_for_unknown_id(self):
        role = RoleEntity(role_id=99, name="Unknown")
        self.assertEqual(role.get_role(), UserRoleEnum.COLLABORATOR)
