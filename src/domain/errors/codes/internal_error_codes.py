from src.domain.errors.models.base_error_code import BaseErrorCode


class InternalErrorCodes(BaseErrorCode):
    SEND_EMAIL_CREATE_AUTH_CODE_ERROR = (500300, "Send email to create auth code error")
    CANNOT_PERSIST_EMAIL_CODE_ERROR = (500301, "Cannot persist email code error")
    VALIDATE_EMAIL_CODE_INTERNAL_ERROR = (500302, "Validate email code internal error")
    CREATE_AUTH_ERROR = (500303, "Create auth internal error")
    LOGIN_INTERNAL_ERROR = (500304, "Login internal error")
    RESET_PASSWORD_ERROR = (500305, "Reset password internal error")
    SEND_EMAIL_FORGET_PASSWORD_CODE_ERROR = (500306, "Send email to forget password code error")
    SEND_EMAIL_VERIFICATION_CODE_ERROR = (500307, "Send email to verification code error")
    UPDATE_PASSWORD_ERROR = (500308, "Update password internal error")
    CREATE_CURRENT_USER_ERROR = (500309, "Create current user internal error")
    GET_CURRENT_USER_ERROR = (500310, "Get current user internal error")
    UPDATE_CURRENT_USER_ERROR = (500312, "Update current user internal error")
    GET_USER_FAMILY_ERROR = (500313, "Get user family internal error")
