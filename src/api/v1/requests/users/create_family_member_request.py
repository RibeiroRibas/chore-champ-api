from pydantic import BaseModel, Field
from pydantic import EmailStr


class CreateFamilyMemberRequest(BaseModel):
    name: str = Field(..., examples=["Jane Doe"])
    email: EmailStr = Field(..., examples=["jane@example.com"])
    phone: str = Field(..., examples=["(48) 99999-9999"])
    role_id: int = Field(..., examples=[2])
    avatar: str | None = Field(None, examples=["👩"])
