from pydantic import BaseModel, Field, EmailStr

class CreateAuthRequest(BaseModel):
    email: EmailStr = Field(..., examples=["ribeiroribas30@gmail.com"])
    email_confirmation_code: int = Field(...)
    password: str = Field(..., min_length=6, examples=['123456'])