from pydantic import BaseModel, Field


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., examples=["550e8400-e29b-41d4-a716-446655440000"])
    current_auth_id: int = Field(..., description="Auth id of the current user", examples=[1])
