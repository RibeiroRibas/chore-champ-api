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
    CHORE_CANNOT_REMOVE_ASSIGNMENT = (400308, "Cannot remove assignment from a chore with no assignee")
    CHORE_CANNOT_COMPLETE = (400309, "Only the assignee or an admin can complete this chore")
    RECURRENCE_DAY_IDS_REQUIRED = (400310, "Recurrence day ids are required")
    ASSIGNED_TO_USER_ID_REQUIRED = (400311, "Assigned to user id is required")
    REWARD_NOT_UNLOCKED = (400312, "Reward is locked for current user")
    ONLY_ADMIN_CAN_REMOVE_CHORE_ASSIGNMENT = (400313, "Only family admins can remove chore assignment")
    COLLABORATOR_CAN_ONLY_COMPLETE_TODAY_CHORES = (400314,"Collaborators can only complete chores that appear in today's list",)
    COLLABORATOR_CREATE_CHORE_MUST_ASSIGN_TO_SELF = (400315,"Collaborators can only create chores assigned to themselves",)
    RECURRING_CHORE_CAN_ONLY_BE_COMPLETED_TODAY = (400316, "Recurring chore can only be completed today.")
    CAN_NOT_CREATE_COMPLETED_RECURRING = (400317, "Can not create completed recurring chore")
    CHORE_CAN_ONLY_BE_COMPLETED_TODAY = (400318, "Chore can only be completed today")