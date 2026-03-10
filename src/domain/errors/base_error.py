class BaseError(Exception):
    def __init__(self, code: int) -> None:
        self.code = code
