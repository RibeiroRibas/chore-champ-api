from src.domain.schemas.entity.auth_entity import AuthEntity
from src.domain.schemas.entity.family_entity import FamilyEntity
from src.domain.schemas.entity.user_entity import UserEntity


class UserAuthFamilyEntity:
    def __init__(self, user_entity: UserEntity, family: FamilyEntity, auth_entity: AuthEntity):
        self.user = user_entity
        self.family = family
        self.auth = auth_entity
