from pydantic import BaseModel, Field

from src.domain.entities.achievement_entity import AchievementEntity


class AchievementResponse(BaseModel):
    id: int = Field(..., examples=[1, 2])
    title: str = Field(..., examples=["Primeiros passos"])
    description: str = Field(..., examples=["Conclua sua primeira tarefa"])
    emoji: str = Field(..., examples=["⭐"])
    required_points: int = Field(..., examples=[5, 50])
    acquired_times: int = Field(..., examples=[0, 3])

    @staticmethod
    def from_entity_with_acquired_times(entity: AchievementEntity, acquired_times: int) -> "AchievementResponse":
        return AchievementResponse(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            emoji=entity.emoji,
            required_points=entity.required_points,
            acquired_times=acquired_times,
        )

