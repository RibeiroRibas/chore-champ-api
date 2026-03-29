from pydantic import BaseModel, Field


class PrivacyPolicyResponse(BaseModel):
    content: str = Field(
        ...,
        examples=["# Privacy Policy\n\n..."],
    )
