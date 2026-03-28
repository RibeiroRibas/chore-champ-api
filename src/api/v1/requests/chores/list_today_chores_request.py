from pydantic import BaseModel, Field


class ListTodayChoresRequest(BaseModel):
    assigned_to_user_id: int | None = Field(
        None,
        description="Filtrar por responsável (id do utilizador). Omitir para todas as tarefas de hoje.",
    )
