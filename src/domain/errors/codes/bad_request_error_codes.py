from src.domain.errors.models.base_error_code import BaseErrorCode


class BadRequestErrorCode(BaseErrorCode):
    SEND_EMAIL_CODE_DISABLED = (400300, "Send email code disabled")
    EMAIL_ALREADY_IN_USE = (400301, "Email already in use")
    USER_ALREADY_REGISTERED_FOR_THIS_AUTH = (400302, "User already registered for this authorization")
    INVALID_PHONE = (400303, "Invalid phone")
    CANNOT_UPDATE_OR_DELETE_CHORE_AFTER_COMPLETED = (400304, "Cannot update or delete chore after completed")