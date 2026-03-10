from pydantic import BaseModel, Field

from src.api.v1.responses.families.family_response import FamilyResponse
from src.api.v1.responses.roles.role_response import RoleResponse
from src.domain.entities.user_family_entity import UserFamilyEntity


class CurrentUserResponse(BaseModel):
    id: int = Field(..., examples=[1, 2])
    name: str = Field(..., examples=["John Doe"])
    auth_id: int = Field(..., examples=[1, 2])
    role: RoleResponse = Field(
        ...,
        examples=[{"id": 1, "name": "Administrador"}],
    )
    phone_number: str = Field(..., examples=["(48) 99641-7323"])
    family: FamilyResponse = Field(
        ...,
        examples=[{"id": 1, "name": "Família Silva"}],
    )

    @staticmethod
    def from_entity(entity: UserFamilyEntity) -> "CurrentUserResponse":
        return CurrentUserResponse(
            id=entity.user.id,
            name=entity.user.name,
            auth_id=entity.user.auth_id,
            role=RoleResponse.from_entity(entity.user.role),
            phone_number=entity.user.phone.formatted(),
            family=FamilyResponse.from_entity(entity.family),
        )