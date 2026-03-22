class FamilyMemberRankingEntity:
    def __init__(
        self,
        id: int,
        name: str,
        points: int,
        role_name: str,
        avatar: str,
    ):
        self.id = id
        self.name = name
        self.points = points
        self.role_name = role_name
        self.avatar = avatar or "👤"
