from src.domain.schemas.entity.family_entity import FamilyEntity
from src.domain.schemas.entity.user_entity import UserEntity
from src.domain.schemas.entity.points_entity import PointsEntity


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
