from src.domain.schemas.entity.family_entity import FamilyEntity
from src.domain.schemas.entity.user_entity import UserEntity


class UserFamilyEntity:
    def __init__(self, user_entity: UserEntity, family: FamilyEntity):
        self.user = user_entity
        self.family = family
