from typing import Any
from pydantic import BaseModel
class HttpBody(BaseModel):
    body: dict[str, Any] = {}

    def to_dict(self) -> dict[str, Any]:
        return self.body
    def add(self, key: str, value: Any) -> 'HttpBody':
        self.body[key] = value
        return self
    def merge(self, other: 'HttpBody') -> 'HttpBody':
        self.body.update(other.body)
        return self