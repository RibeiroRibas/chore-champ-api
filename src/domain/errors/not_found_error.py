from src.domain.errors.base_error import BaseError


class NotFoundError(BaseError):
    
    def __init__(self, code: int):
        super().__init__(code)
        
    
    def get_code(self) -> int:
        return self.code