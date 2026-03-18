from src.domain.entities.family_entity import FamilyEntity
from src.domain.entities.user_entity import UserEntity
from src.domain.entities.user_points_entity import UserPointsEntity


class UserPointsFamilyEntity:
    def __init__(
        self,
        user: UserEntity,
        family: FamilyEntity,
        user_points: UserPointsEntity | None,
    ):
        self.user = user
        self.family = family
        self.user_points = user_points

    def available_points(self) -> int:
        return self.user_points.available_points() if self.user_points else 0
