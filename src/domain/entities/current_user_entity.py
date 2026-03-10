from src.domain.entities.role_entity import RoleEntity
from src.domain.vo.phone import PhoneVO


class CurrentUserEntity:
    def __init__(self, user_id: int, auth_id: int, role_id: int, family_id: int):
        self.user_id = user_id
        self.auth_id = auth_id
        self.role_id = role_id
        self.family_id = family_id
