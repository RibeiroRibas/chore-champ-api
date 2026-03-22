from pydantic import BaseModel, Field

from src.domain.schemas.entity.family_member_ranking_entity import FamilyMemberRankingEntity


class FamilyMemberRankingResponse(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Jane Doe"])
    points: int = Field(..., examples=[120])
    role_name: str = Field(..., examples=["Colaborador"])
    avatar: str = Field(default="👤", examples=["👩"])

    @staticmethod
    def from_entity(entity: FamilyMemberRankingEntity) -> "FamilyMemberRankingResponse":
        return FamilyMemberRankingResponse(
            id=entity.id,
            name=entity.name,
            points=entity.points,
            role_name=entity.role_name,
            avatar=entity.avatar,
        )
