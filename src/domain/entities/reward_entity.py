class RewardEntity:
    def __init__(
        self,
        reward_id: int,
        title: str,
        subtitle: str | None,
        emoji: str,
        achievement_id: int,
        required_points: int | None = None,
    ):
        self.id = reward_id
        self.title = title
        self.subtitle = subtitle
        self.emoji = emoji
        self.achievement_id = achievement_id
        self.required_points = required_points

    def is_unlocked(self, available_points: int) -> bool:
        if self.required_points is None:
            return False
        return available_points >= self.required_points

    def validate_can_claim(self, available_points: int) -> None:
        from src.domain.errors.bad_request_error import BadRequestError
        from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode

        if not self.is_unlocked(available_points=available_points):
            raise BadRequestError(code=BadRequestErrorCode.REWARD_NOT_UNLOCKED.code())
