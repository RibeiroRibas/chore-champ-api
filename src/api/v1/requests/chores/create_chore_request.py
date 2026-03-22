from pydantic import BaseModel, Field, model_validator


class CreateChoreRequest(BaseModel):
    title: str = Field(..., examples=["Lavar a louça"])
    emoji: str = Field(default="🧹", examples=["🧹"])
    points: int = Field(..., examples=[10])
    assigned_to_user_ids: list[int] = Field(
        default_factory=list,
        examples=[[2, 3]],
        description="IDs dos membros; uma tarefa é criada por ID. Lista vazia = tarefa sem responsável.",
    )
    completed: bool = Field(default=False)
    is_recurring: bool = Field(default=False, examples=[False])
    recurrence_day_ids: list[int] | None = Field(None, examples=[[1, 3, 5]])
