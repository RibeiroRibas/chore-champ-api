from pydantic import BaseModel, Field

from src.domain.schemas.entity.day_of_week_entity import DayOfWeekEntity


class DayOfWeekResponse(BaseModel):
    id: int = Field(..., description="ID do dia da semana (1=Segunda .. 7=Domingo)", examples=[1])
    name: str = Field(..., description="Nome do dia", examples=["Segunda"])

    @staticmethod
    def from_entity(entity: DayOfWeekEntity) -> "DayOfWeekResponse":
        return DayOfWeekResponse(id=entity.id, name=entity.name)
