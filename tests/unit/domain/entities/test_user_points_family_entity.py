import unittest

from src.domain.entities.family_entity import FamilyEntity
from src.domain.entities.points_entity import PointsEntity
from src.domain.entities.role_entity import RoleEntity
from src.domain.entities.user_entity import UserEntity
from src.domain.entities.user_points_family_entity import UserPointsFamilyEntity


class TestUserPointsFamilyEntity(unittest.TestCase):
    def _user(self, user_id: int = 1) -> UserEntity:
        return UserEntity(
            user_id=user_id,
            name="Maria",
            auth_id=10,
            role=RoleEntity(role_id=1, name="Admin"),
            phone_number="11999999999",
        )

    def _family(self) -> FamilyEntity:
        return FamilyEntity(id=1, name="Família Silva")

    def _points(self, total: int = 80, redeemed: int = 10) -> PointsEntity:
        return PointsEntity(
            id=1,
            total_points=total,
            user_id=1,
            points_redeemed=redeemed,
            family_id=1,
        )

    def test_available_points_returns_points_when_points_exists(self):
        entity = UserPointsFamilyEntity(
            user=self._user(),
            family=self._family(),
            points=self._points(total=80, redeemed=10),
        )
        self.assertEqual(entity.available_points(), 70)

    def test_available_points_returns_zero_when_points_is_none(self):
        entity = UserPointsFamilyEntity(
            user=self._user(),
            family=self._family(),
            points=None,
        )
        self.assertEqual(entity.available_points(), 0)
