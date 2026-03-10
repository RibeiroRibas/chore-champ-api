from pydantic import BaseModel, Field

from src.domain.entities.family_entity import FamilyEntity


class FamilyResponse(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Família Silva"])

    @staticmethod
    def from_entity(entity: FamilyEntity) -> "FamilyResponse":
        return FamilyResponse(id=entity.id, name=entity.name)
