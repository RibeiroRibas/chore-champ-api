import unittest

from src.domain.entities.achievement_entity import AchievementEntity
from src.domain.entities.points_entity import PointsEntity
from src.domain.entities.role_entity import RoleEntity
from src.domain.entities.user_entity import UserEntity
from src.domain.entities.user_points_achievements_entity import UserPointsAchievementsEntity


class TestUserPointsAchievementsEntity(unittest.TestCase):
    def _user(self, user_id: int = 1) -> UserEntity:
        return UserEntity(
            user_id=user_id,
            name="João",
            auth_id=10,
            role=RoleEntity(role_id=1, name="Admin"),
            phone_number="11999999999",
        )

    def _points(self, total: int = 100, redeemed: int = 20) -> PointsEntity:
        return PointsEntity(
            id=1,
            total_points=total,
            user_id=1,
            points_redeemed=redeemed,
            family_id=1,
        )

    def _achievement(self, achievement_id: int = 1) -> AchievementEntity:
        return AchievementEntity(
            achievement_id=achievement_id,
            title="Primeira tarefa",
            description="Complete uma tarefa",
            emoji="🎯",
            required_points=10,
        )

    def test_available_points_returns_points_when_points_exists(self):
        user = self._user()
        points = self._points(total=100, redeemed=30)
        entity = UserPointsAchievementsEntity(
            user=user,
            points=points,
            achievements=[],
        )
        self.assertEqual(entity.available_points(), 70)

    def test_available_points_returns_zero_when_points_is_none(self):
        user = self._user()
        entity = UserPointsAchievementsEntity(
            user=user,
            points=None,
            achievements=[],
        )
        self.assertEqual(entity.available_points(), 0)

    def test_calculate_how_many_times_achievements_was_acquired_returns_count(self):
        ach = self._achievement(achievement_id=5)
        ach2 = AchievementEntity(
            achievement_id=5,
            title="x",
            description="x",
            emoji="x",
            required_points=5,
        )
        ach3 = AchievementEntity(
            achievement_id=99,
            title="y",
            description="y",
            emoji="y",
            required_points=5,
        )
        entity = UserPointsAchievementsEntity(
            user=self._user(),
            points=None,
            achievements=[ach2, ach2, ach3],
        )
        self.assertEqual(entity.calculate_how_many_times_achievements_was_acquired(ach), 2)

    def test_calculate_how_many_times_achievements_was_acquired_returns_zero_when_none(self):
        ach = self._achievement(achievement_id=5)
        entity = UserPointsAchievementsEntity(
            user=self._user(),
            points=None,
            achievements=[],
        )
        self.assertEqual(entity.calculate_how_many_times_achievements_was_acquired(ach), 0)

    def test_calculate_how_many_times_achievements_was_acquired_handles_none_achievements(self):
        ach = self._achievement(achievement_id=5)
        entity = UserPointsAchievementsEntity(
            user=self._user(),
            points=None,
            achievements=None,
        )
        self.assertEqual(entity.calculate_how_many_times_achievements_was_acquired(ach), 0)
