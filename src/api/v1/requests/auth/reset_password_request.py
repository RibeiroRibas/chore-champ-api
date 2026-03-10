from pydantic import BaseModel, Field, EmailStr


class ResetPasswordRequest(BaseModel):
    confirmation_code: int = Field(..., description="The confirmation code")
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)