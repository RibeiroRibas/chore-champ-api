from src.domain.enums.user_role_enum import UserRoleEnum


class RoleEntity:
    def __init__(self, role_id, name):
        self.id = role_id
        self.name = name

    def get_role(self) -> UserRoleEnum:
        return UserRoleEnum.ADMIN if self.id == UserRoleEnum.ADMIN.value[0] else UserRoleEnum.COLLABORATOR
