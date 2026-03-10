from pydantic import BaseModel, Field, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["ribeiroribas30@gmail.com"])
    password: str = Field(..., examples=['123456'])