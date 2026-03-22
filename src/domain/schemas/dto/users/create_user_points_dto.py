from dataclasses import dataclass


@dataclass
class CreateUserPointsDTO:
    user_id: int
    family_id: int
    total_points: int
