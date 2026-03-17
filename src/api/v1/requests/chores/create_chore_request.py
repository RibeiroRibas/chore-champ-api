from pydantic import BaseModel, Field


class CreateChoreRequest(BaseModel):
    title: str = Field(..., examples=["Lavar a louça"])
    emoji: str = Field(default="🧹", examples=["🧹"])
    points: int = Field(..., examples=[10])
    assigned_to_user_id: int | None = Field(None, examples=[2])
    completed: bool = Field(default=False)
    is_recurring: bool = Field(default=False, examples=[False])
    recurrence_day_ids: list[int] | None = Field(None, examples=[[1, 3, 5]])
