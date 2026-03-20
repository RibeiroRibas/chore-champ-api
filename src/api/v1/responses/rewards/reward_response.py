from pydantic import BaseModel, Field

from src.domain.entities.reward_entity import RewardEntity


class RewardResponse(BaseModel):
    id: int = Field(..., examples=[1])
    title: str = Field(..., examples=["Tempo extra de tela"])
    subtitle: str | None = Field(None, examples=["30 minutos de bonus"])
    emoji: str = Field(..., examples=["🎁"])
    achievement_id: int = Field(..., examples=[2])
    required_points: int = Field(..., examples=[100])
    unlocked: bool = Field(..., examples=[False, True])

    @staticmethod
    def from_entity(entity: RewardEntity, available_points: int) -> "RewardResponse":
        return RewardResponse(
            id=entity.id,
            title=entity.title,
            subtitle=entity.subtitle,
            emoji=entity.emoji,
            achievement_id=entity.achievement_id,
            required_points=entity.required_points or 0,
            unlocked=entity.is_unlocked(available_points=available_points),
        )
