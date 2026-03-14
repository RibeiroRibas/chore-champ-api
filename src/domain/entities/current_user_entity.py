from src.domain.enums.user_role_enum import UserRoleEnum


class CurrentUserEntity:
    def __init__(self, user_id: int, auth_id: int, role_id: int, family_id: int):
        self.user_id = user_id
        self.auth_id = auth_id
        self.role_id = role_id
        self.family_id = family_id

    def is_admin(self) -> bool:
        return self.role_id == UserRoleEnum.ADMIN.value[0]
