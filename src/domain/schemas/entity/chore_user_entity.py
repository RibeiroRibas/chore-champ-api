from src.domain.schemas.entity.chore_entity import ChoreEntity
from src.domain.schemas.entity.user_entity import UserEntity


class ChoreUserEntity:
    def __init__(self, user_entity: UserEntity | None, chore: ChoreEntity):
        self.user = user_entity
        self.chore = chore
