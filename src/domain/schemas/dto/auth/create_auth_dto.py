from dataclasses import dataclass


@dataclass
class CreateAuthDTO:
    username: str
    password: str