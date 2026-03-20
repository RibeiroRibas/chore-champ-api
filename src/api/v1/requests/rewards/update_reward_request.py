from pydantic import BaseModel, Field


class UpdateRewardRequest(BaseModel):
    title: str = Field(..., examples=["Pular uma tarefa"])
    subtitle: str | None = Field(None, examples=["Passe livre para uma tarefa"])
    emoji: str = Field(..., examples=["🎟️"])
    achievement_id: int = Field(..., examples=[3])
