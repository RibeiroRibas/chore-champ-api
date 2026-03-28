class FamilyMemberRankingEntity:
    def __init__(
        self,
        id: int,
        name: str,
        ranking_points: int,
        available_points: int,
        role_name: str,
        avatar: str,
    ):
        self.id = id
        self.name = name
        self.ranking_points = ranking_points
        self.available_points = available_points
        self.role_name = role_name
        self.avatar = avatar or "👤"
