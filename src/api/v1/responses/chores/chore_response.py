from pydantic import BaseModel, Field

from src.domain.entities.chore_entity import ChoreEntity


class ChoreResponse(BaseModel):
    id: int = Field(..., examples=[1])
    title: str = Field(..., examples=["Lavar a louça"])
    emoji: str = Field(..., examples=["🧹"])
    points: int = Field(..., examples=[10])
    assigned_to: int | None = Field(None, examples=[2])
    created_by: int = Field(..., examples=[1])
    completed: bool = Field(..., examples=[False])

    @staticmethod
    def from_entity(entity: ChoreEntity) -> "ChoreResponse":
        return ChoreResponse(
            id=entity.id,
            title=entity.title,
            emoji=entity.emoji,
            points=entity.points,
            assigned_to=entity.assigned_to_user_id,
            created_by=entity.created_by_user_id,
            completed=entity.completed,
        )
