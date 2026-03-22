from src.domain.schemas.entity.achievement_entity import AchievementEntity
from src.domain.schemas.entity.points_entity import PointsEntity
from src.domain.schemas.entity.user_entity import UserEntity


class UserPointsAchievementsEntity:
    def __init__(
        self,
        user: UserEntity,
        points: PointsEntity | None,
        achievements: list[AchievementEntity] | None
    ):
        self.user = user
        self.achievements = achievements
        self.points = points

    def available_points(self) -> int:
        return self.points.available_points() if self.points else 0

    def calculate_how_many_times_achievements_was_acquired(self, achievement: AchievementEntity) -> int:
        return sum(1 for ach in (self.achievements or []) if achievement.id == ach.id)

