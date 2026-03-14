from src.api.v1.docs.models.api_error_docs import build_doc_errors_response
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes

list_family_members = {
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.FAMILY_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.LIST_FAMILY_MEMBERS_ERROR,
        ]
    ),
}

create_family_member = {
    400: build_doc_errors_response(
        [
            BadRequestErrorCode.EMAIL_ALREADY_IN_USE,
            BadRequestErrorCode.INVALID_PHONE,
        ]
    ),
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.INSUFFICIENT_PERMISSIONS,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.FAMILY_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.CREATE_FAMILY_MEMBER_ERROR,
        ]
    ),
}

get_family_member = {
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.USER_NOT_FOUND,
            NotFoundErrorCodes.FAMILY_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.GET_FAMILY_MEMBER_ERROR,
        ]
    ),
}

update_family_member = {
    400: build_doc_errors_response(
        [
            BadRequestErrorCode.INVALID_PHONE,
            BadRequestErrorCode.FAMILY_MUST_HAVE_AT_LEAST_ONE_ADMIN
        ]
    ),
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.INSUFFICIENT_PERMISSIONS,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.USER_NOT_FOUND,
            NotFoundErrorCodes.FAMILY_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.UPDATE_FAMILY_MEMBER_ERROR,
        ]
    ),
}

delete_family_member = {
    400: build_doc_errors_response(
        [
            BadRequestErrorCode.FAMILY_MUST_HAVE_AT_LEAST_ONE_ADMIN
        ]
    ),
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.INSUFFICIENT_PERMISSIONS,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.USER_NOT_FOUND,
            NotFoundErrorCodes.FAMILY_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.DELETE_FAMILY_MEMBER_ERROR,
        ]
    ),
}

resend_family_member_password = {
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.INSUFFICIENT_PERMISSIONS,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
            NotFoundErrorCodes.USER_NOT_FOUND,
            NotFoundErrorCodes.FAMILY_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.RESEND_FAMILY_MEMBER_PASSWORD_ERROR,
        ]
    ),
}
