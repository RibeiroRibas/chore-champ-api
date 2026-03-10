from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import jwt
import os

from dotenv import load_dotenv

from src.domain.errors.unauthorized_error import UnauthorizedError
from src.infra.http.errors.codes.infra_error_codes import InfraErrorCodes

load_dotenv()

class JWTService:
    
    def __init__(self):
        self.secret_key = os.getenv("AUTH_ACCESS_TOKEN_SECRET_KEY")
        self.algorithm = os.getenv("AUTH_ACCESS_TOKEN_ALGORITHM", "HS256")
        self.default_expiration_minutes = int(os.getenv("AUTH_EXPIRES_ACCESS_TOKEN_IN_MINUTES", "60"))

    def generate_token(self, auth_id: int) -> str:
        token_payload = {
            'auth_id': auth_id,
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + timedelta(minutes=self.default_expiration_minutes)
        }
        
        token = jwt.encode(
            token_payload,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        return token


    def validate_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError(code=InfraErrorCodes.EXPIRED_TOKEN.code())
        except jwt.InvalidTokenError:
            raise UnauthorizedError(code=InfraErrorCodes.INVALID_TOKEN.code())
        
    
    def decode_auth_id_from_token(self, token: str) -> int:
        payload = self.validate_token(token)
        return payload.get('auth_id')
    