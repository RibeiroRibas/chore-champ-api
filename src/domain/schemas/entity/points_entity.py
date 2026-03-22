class PointsEntity:
    def __init__(
        self,
        id: int,
        total_points: int,
        user_id: int,
        points_redeemed: int,
        family_id: int,
    ):
        self.id = id
        self.total_points = total_points
        self.user_id = user_id
        self.points_redeemed = points_redeemed
        self.family_id = family_id

    def available_points(self) -> int:
        return self.total_points - self.points_redeemed
