from pydantic import BaseModel, Field


class CreateCurrentUserRequest(BaseModel):
    name: str = Field(..., examples=["John Doe"])
    phone: str = Field(..., examples=['(48) 996417323'])
    family_name: str = Field(..., examples=["Silva Family"])
