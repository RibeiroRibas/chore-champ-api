from dataclasses import dataclass

from src.domain.vo.phone import PhoneVO


@dataclass
class UpdateUserDTO:
    name: str
    phone: PhoneVO
    avatar: str | None = None