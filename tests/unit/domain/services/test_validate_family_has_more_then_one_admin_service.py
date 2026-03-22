import unittest
from unittest.mock import MagicMock

from src.domain.schemas.entity.family_entity import FamilyEntity
from src.domain.schemas.entity.user_entity import UserEntity
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.internal_error import InternalError
from src.domain.services.validate_family_has_more_then_one_admin_service import (
    ValidateFamilyMoreThenOneAdminService,
)


class TestValidateFamilyMoreThenOneAdminService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = ValidateFamilyMoreThenOneAdminService(
            family_repository=self.mock_repo
        )

    def test_execute_passes_when_at_least_two_admins(self):
        member1 = MagicMock(spec=UserEntity)
        member2 = MagicMock(spec=UserEntity)
        family = FamilyEntity(id=1, name="Family", members=[member1, member2])
        self.mock_repo.find_admin_members.return_value = family
        self.service.execute(family_id=1)
        self.mock_repo.find_admin_members.assert_called_once_with(1)

    def test_execute_passes_when_more_than_two_admins(self):
        members = [MagicMock(spec=UserEntity) for _ in range(5)]
        family = FamilyEntity(id=1, name="Family", members=members)
        self.mock_repo.find_admin_members.return_value = family
        self.service.execute(family_id=1)

    def test_execute_raises_bad_request_when_family_is_none(self):
        self.mock_repo.find_admin_members.return_value = None
        with self.assertRaises(BadRequestError):
            self.service.execute(family_id=1)

    def test_execute_raises_bad_request_when_only_one_admin(self):
        family = FamilyEntity(id=1, name="Family", members=[MagicMock()])
        self.mock_repo.find_admin_members.return_value = family
        with self.assertRaises(BadRequestError):
            self.service.execute(family_id=1)

    def test_execute_raises_bad_request_when_zero_admins(self):
        family = FamilyEntity(id=1, name="Family", members=[])
        self.mock_repo.find_admin_members.return_value = family
        with self.assertRaises(BadRequestError):
            self.service.execute(family_id=1)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.not_found_error import NotFoundError
        self.mock_repo.find_admin_members.side_effect = NotFoundError(code=404)
        with self.assertRaises(NotFoundError):
            self.service.execute(family_id=1)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_repo.find_admin_members.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.service.execute(family_id=1)
