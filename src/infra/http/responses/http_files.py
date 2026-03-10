from typing import Any

from pydantic import BaseModel, Field


class HttpFiles(BaseModel):
    files: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.files.copy()

    def add(self, key: str, value: Any) -> 'HttpFiles':
        self.files[key] = value
        return self

    def merge(self, other: 'HttpFiles') -> 'HttpFiles':
        self.files.update(other.files)
        return self
