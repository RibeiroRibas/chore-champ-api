from src.domain.services.b_crypt_password_service import verify_password


class AuthEntity:
    def __init__(self, id: int, username: str, password: str):
        self.id = id
        self.username = username
        self.password = password

    def is_password_equals(self, plain_password: str) -> bool:
        return verify_password(plain_password, self.password)

