from pydantic import BaseModel, Field


class UpdateFamilyMemberRequest(BaseModel):
    name: str = Field(..., examples=["Jane Doe"])
    email: str = Field(..., examples=["jane@example.com"])
    phone: str = Field(..., examples=["(48) 99999-9999"])
    role_id: int = Field(..., examples=[1, 2])
    avatar: str | None = Field(None, examples=["👩"])
