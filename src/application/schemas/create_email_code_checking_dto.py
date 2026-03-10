from dataclasses import dataclass


@dataclass
class CreateEmailCodeCheckingDTO:
    email: str
    code: str