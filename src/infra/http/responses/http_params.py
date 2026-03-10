from typing import Any
from pydantic import BaseModel
class HttpParams(BaseModel):
    params: dict[str, Any] = {}

    def to_dict(self) -> dict[str, Any]:
        return self.params
    def add(self, key: str, value: Any) -> 'HttpParams':
        self.params[key] = value
        return self
    def merge(self, other: 'HttpParams') -> 'HttpParams':
        self.params.update(other.params)
        return self