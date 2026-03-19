class AchievementEntity:
    def __init__(
        self,
        achievement_id: int,
        title: str,
        description: str,
        emoji: str,
        required_points: int,
    ):
        self.id = achievement_id
        self.title = title
        self.description = description
        self.emoji = emoji
        self.required_points = required_points

