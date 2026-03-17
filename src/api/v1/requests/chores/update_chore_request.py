from pydantic import BaseModel, Field


class UpdateChoreRequest(BaseModel):
    title: str | None = Field(None, examples=["Lavar a louça"])
    emoji: str | None = Field(None, examples=["🧹"])
    points: int | None = Field(None, examples=[10])
    assigned_to_user_id: int | None = Field(None, examples=[2])
    completed: bool = Field(default=False)
    is_recurring: bool | None = Field(None)
    recurrence_day_ids: list[int] | None = Field(None, examples=[[1, 3, 5]])
