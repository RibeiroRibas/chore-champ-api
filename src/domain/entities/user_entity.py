from src.domain.entities.role_entity import RoleEntity
from src.domain.vo.phone import PhoneVO


class UserEntity:
    def __init__(
        self,
        id: int,
        name: str,
        auth_id: int,
        role: RoleEntity,
        phone_number: str,
        email: str | None = None,
        avatar: str | None = None,
    ):
        self.id = id
        self.name = name
        self.auth_id = auth_id
        self.role = role
        self.phone = PhoneVO(phone_number)
        self.email = email
        self.avatar = avatar
