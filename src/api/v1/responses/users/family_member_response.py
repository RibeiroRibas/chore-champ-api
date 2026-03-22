from pydantic import BaseModel, Field

from src.domain.schemas.entity.user_entity import UserEntity


class FamilyMemberResponse(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Jane Doe"])
    email: str = Field(..., examples=["jane@example.com"])
    phone_number: str = Field(..., examples=["(48) 99999-9999"])
    role_id: int = Field(..., examples=[2])
    role_name: str = Field(..., examples=["Colaborador"])
    avatar: str = Field(default="👤", examples=["👩"])

    @staticmethod
    def from_user_entity(entity: UserEntity) -> 'FamilyMemberResponse':
        return FamilyMemberResponse(
            id=entity.id,
            name=entity.name,
            phone_number=entity.phone.formatted(),
            email=entity.email or "",
            role_id=entity.role.id,
            role_name=entity.role.name,
            avatar=entity.avatar or "👤",
        )
