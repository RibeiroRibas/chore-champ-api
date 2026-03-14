from src.domain.errors.models.base_error_code import BaseErrorCode


class BadRequestErrorCode(BaseErrorCode):
    SEND_EMAIL_CODE_DISABLED = (400300, "Send email code disabled")
    EMAIL_ALREADY_IN_USE = (400301, "Email already in use")
    USER_ALREADY_REGISTERED_FOR_THIS_AUTH = (400302, "User already registered for this authorization")
    INVALID_PHONE = (400303, "Invalid phone")
    CANNOT_UPDATE_OR_DELETE_CHORE_AFTER_COMPLETED = (400304, "Cannot update or delete chore after completed")
    FAMILY_MUST_HAVE_AT_LEAST_ONE_ADMIN = (400305, "Family must have at least one admin")
    CHORE_ALREADY_ASSIGNED = (400306, "Chore already has an assignee; only admins can reassign")
    CHORE_ALREADY_COMPLETED = (400307, "Cannot assign a completed chore")
    CHORE_CANNOT_REMOVE_ASSIGNMENT = (400308, "Can only remove assignment from a chore assigned to you and not completed")
    CHORE_CANNOT_COMPLETE = (400309, "Only the assignee or an admin can complete this chore")