from src.api.v1.docs.models.api_error_docs import build_doc_errors_response
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes


list_today_chores = {
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.LIST_CHORES_ERROR,
        ]
    ),
}


list_all_chores = {
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.LIST_CHORES_ERROR,
        ]
    ),
}


create_chore = {
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.CREATE_CHORE_ERROR,
        ]
    ),
}


get_chore = {
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.CHORE_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.GET_CHORE_ERROR,
        ]
    ),
}


update_chore = {
    400: build_doc_errors_response(
        [
            BadRequestErrorCode.CANNOT_UPDATE_OR_DELETE_CHORE_AFTER_COMPLETED,
        ]
    ),
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.CURRENT_USER_CANNOT_UPDATE_CHORE,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.CHORE_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.UPDATE_CHORE_ERROR,
            InternalErrorCodes.GET_USER_FAMILY_ERROR,
        ]
    ),
}


delete_chore = {
    400: build_doc_errors_response(
        [
            BadRequestErrorCode.CANNOT_UPDATE_OR_DELETE_CHORE_AFTER_COMPLETED,
        ]
    ),
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.CURRENT_USER_CANNOT_UPDATE_CHORE,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.CHORE_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.DELETE_CHORE_ERROR,
            InternalErrorCodes.GET_USER_FAMILY_ERROR,
        ]
    ),
}

assign_chore_to_me = {
    400: build_doc_errors_response(
        [
            BadRequestErrorCode.CHORE_ALREADY_ASSIGNED,
            BadRequestErrorCode.CHORE_ALREADY_COMPLETED,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.CHORE_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.ASSIGN_CHORE_TO_ME_ERROR,
            InternalErrorCodes.GET_USER_FAMILY_ERROR,
        ]
    ),
}

remove_assign_chore_to_me = {
    400: build_doc_errors_response(
        [
            BadRequestErrorCode.CHORE_ALREADY_COMPLETED,
            BadRequestErrorCode.CHORE_CANNOT_REMOVE_ASSIGNMENT,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.CHORE_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.REMOVE_ASSIGN_CHORE_TO_ME_ERROR,
            InternalErrorCodes.GET_USER_FAMILY_ERROR,
        ]
    ),
}

complete_chore = {
    400: build_doc_errors_response(
        [
            BadRequestErrorCode.CHORE_ALREADY_COMPLETED,
            BadRequestErrorCode.CHORE_CANNOT_COMPLETE,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.CHORE_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.COMPLETE_CHORE_ERROR,
            InternalErrorCodes.GET_USER_FAMILY_ERROR,
        ]
    ),
}

