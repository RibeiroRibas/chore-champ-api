from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.infra.services.jwt_service import JWTService

__security_scheme = HTTPBearer()
__jwt_service = JWTService()

def get_current_auth_id(credentials: Annotated[HTTPAuthorizationCredentials, Depends(__security_scheme)]) -> int:
    token = credentials.credentials
    return __jwt_service.decode_auth_id_from_token(token=token)
