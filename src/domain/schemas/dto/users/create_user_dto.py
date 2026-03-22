from dataclasses import dataclass

from src.domain.vo.phone import PhoneVO


@dataclass
class CreateUserDTO:
    name: str
    auth_id: int
    role_id: int
    phone: PhoneVO
    family_id: int
    avatar: str | None = None