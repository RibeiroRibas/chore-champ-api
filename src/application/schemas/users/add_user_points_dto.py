from dataclasses import dataclass


@dataclass
class AddUserPointsDTO:
    user_id: int
    points: int
    family_id: int
