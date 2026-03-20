from dataclasses import dataclass


@dataclass
class UpdateRewardDTO:
    title: str
    subtitle: str | None
    emoji: str
    achievement_id: int
