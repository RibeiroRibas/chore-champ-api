from src.domain.entities.user_entity import UserEntity


class FamilyEntity:
    def __init__(self, id: int, name: str, members: list[UserEntity] | None = None):
        self.id = id
        self.name = name
        self.members = members if members is not None else []
