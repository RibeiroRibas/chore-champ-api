from pydantic import BaseModel, Field

from src.domain.schemas.entity.family_member_ranking_entity import FamilyMemberRankingEntity


class FamilyMemberRankingResponse(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Jane Doe"])
    ranking_points: int = Field(
        ...,
        examples=[200],
        description="Lifetime points earned; used for ranking order (monotonic).",
    )
    available_points: int = Field(
        ...,
        examples=[120],
        description="Balance for claiming rewards (total minus redeemed).",
    )
    role_name: str = Field(..., examples=["Colaborador"])
    avatar: str = Field(default="👤", examples=["👩"])

    @staticmethod
    def from_entity(entity: FamilyMemberRankingEntity) -> "FamilyMemberRankingResponse":
        return FamilyMemberRankingResponse(
            id=entity.id,
            name=entity.name,
            ranking_points=entity.ranking_points,
            available_points=entity.available_points,
            role_name=entity.role_name,
            avatar=entity.avatar,
        )
