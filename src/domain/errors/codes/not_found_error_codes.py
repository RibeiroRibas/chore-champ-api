from src.domain.errors.models.base_error_code import BaseErrorCode


class NotFoundErrorCodes(BaseErrorCode):
    EMAIL_CODE_CHECKING_NOT_FOUND = (404300, "Email code checking error during HTTP request")
    USER_NOT_FOUND = (404301, "User not found")
    AUTH_NOT_FOUND = (404302, "Auth not found")
    ROLE_NOT_FOUND = (404303, "Role not found")
    FAMILY_NOT_FOUND = (404304, "Family not found")
