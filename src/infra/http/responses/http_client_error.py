from pydantic import BaseModel

class HttpClientError(BaseModel):
    code: int
    message: str