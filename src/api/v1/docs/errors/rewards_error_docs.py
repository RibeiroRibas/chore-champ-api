from src.api.v1.docs.models.api_error_docs import build_doc_errors_response
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes


list_rewards = {
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.LIST_REWARDS_ERROR,
        ]
    ),
}

create_reward = {
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.INSUFFICIENT_PERMISSIONS,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.ACHIEVEMENT_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.CREATE_REWARD_ERROR,
        ]
    ),
}

get_reward = {
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.REWARD_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.GET_REWARD_ERROR,
        ]
    ),
}

update_reward = {
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.INSUFFICIENT_PERMISSIONS,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.REWARD_NOT_FOUND,
            NotFoundErrorCodes.ACHIEVEMENT_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.UPDATE_REWARD_ERROR,
        ]
    ),
}

delete_reward = {
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.INSUFFICIENT_PERMISSIONS,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.REWARD_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.DELETE_REWARD_ERROR,
        ]
    ),
}

claim_reward = {
    400: build_doc_errors_response(
        [
            BadRequestErrorCode.REWARD_NOT_UNLOCKED,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.REWARD_NOT_FOUND,
            NotFoundErrorCodes.USER_POINTS_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.CLAIM_REWARD_ERROR,
        ]
    ),
}
