from dataclasses import dataclass


@dataclass
class CreateRewardDTO:
    title: str
    subtitle: str | None
    emoji: str
    achievement_id: int
