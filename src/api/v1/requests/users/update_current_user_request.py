from pydantic import BaseModel, Field

class UpdateCurrentUserRequest(BaseModel):
    name: str = Field(..., examples=["John Doe"])
    phone: str = Field(..., examples=['(48) 996417323'])
