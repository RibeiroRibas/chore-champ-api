from src.domain.errors.models.base_error_code import BaseErrorCode


class UnauthorizedErrorCodes(BaseErrorCode):
    EMAIL_CODE_VALIDATED = (401300, "Email code validation error")
    EMAIL_CODE_EXPIRED = (401301, "Email code expiration error")
    EMAIL_CODE_BLOCKED = (401302, "Email code blocked error")
    EMAIL_CODE_INVALID =(401303, "Email code invalid error")
    INVALID_USER_CREDENTIALS = (401304, "Invalid user credentials")
    INSUFFICIENT_PERMISSIONS = (401305, "Insufficient permissions")

