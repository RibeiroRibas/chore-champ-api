from typing import Optional, TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar('T')


class HttpResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    status_code: Optional[int] = None
    status_message: Optional[str] = None
    text: Optional[str] = None
    headers: dict[str, str] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True
    
    def is_success(self) -> bool:
        return self.status_code is not None and 200 <= self.status_code < 300
    
    def is_client_error(self) -> bool:
        return self.status_code is not None and 400 <= self.status_code < 500
    
    def is_server_error(self) -> bool:
        return self.status_code is not None and self.status_code >= 500

    def has_error(self) -> bool:
        return not self.is_success()
