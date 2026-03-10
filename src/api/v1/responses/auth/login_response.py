from typing import Optional

from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    access_token: str = Field(...)
    refresh_token: Optional[str] = Field(None)
