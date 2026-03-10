from pydantic import BaseModel, Field


class HttpHeaders(BaseModel):
    headers: dict[str, str] = Field(default_factory=dict)
    
    def to_dict(self) -> dict[str, str]:
        return self.headers.copy()
    
    def add(self, key: str, value: str) -> 'HttpHeaders':
        self.headers[key] = value
        return self
    
    def merge(self, other: 'HttpHeaders') -> 'HttpHeaders':
        self.headers.update(other.headers)
        return self
