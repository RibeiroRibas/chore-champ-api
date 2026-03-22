from pydantic import BaseModel, Field

from src.domain.schemas.entity.role_entity import RoleEntity


class RoleResponse(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=['Administrador'])

    @staticmethod
    def from_entity(entity: RoleEntity) -> 'RoleResponse':
        return RoleResponse(
            id=entity.id,
            name=entity.name
        )