from src.domain.entities.family_entity import FamilyEntity
from src.domain.entities.user_entity import UserEntity
from src.domain.entities.points_entity import PointsEntity


class UserPointsFamilyEntity:
    def __init__(
        self,
        user: UserEntity,
        family: FamilyEntity,
        points: PointsEntity | None,
    ):
        self.user = user
        self.family = family
        self.points = points

    def available_points(self) -> int:
        return self.points.available_points() if self.points else 0
