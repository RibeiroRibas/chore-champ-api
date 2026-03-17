from pydantic import BaseModel, Field


class GetChoresFilteredRequest(BaseModel):
    completed: bool | None = Field(None, description="Filtrar por concluída")
    is_recurring: bool | None = Field(None, description="Filtrar por recorrente")
    title: str | None = Field(None, description="Filtrar por trecho do título")
    assigned_to_user_id: int | None = Field(None, description="Filtrar por utilizador atribuído")
    page_size: int = Field(20, ge=1, le=100, description="Tamanho da página")
    page: int = Field(1, ge=1, description="Página atual")
