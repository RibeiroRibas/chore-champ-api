from src.domain.errors.base_error import BaseError


class UnauthorizedError(BaseError):

    def __init__(self, code: int) -> None:
        super().__init__(code)

    def get_code(self) -> int:
        return self.code
