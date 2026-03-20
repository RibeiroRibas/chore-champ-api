from pydantic import BaseModel, Field


class CreateRewardRequest(BaseModel):
    title: str = Field(..., examples=["Tempo extra de tela"])
    subtitle: str | None = Field(None, examples=["30 minutos de bonus"])
    emoji: str = Field(..., examples=["🎁"])
    achievement_id: int = Field(..., examples=[2])
