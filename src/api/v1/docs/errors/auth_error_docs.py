from src.api.v1.docs.models.api_error_docs import build_doc_errors_response
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes
from src.infra.http.errors.codes.infra_error_codes import InfraErrorCodes

create_auth = {
    400: build_doc_errors_response(
        [
            BadRequestErrorCode.EMAIL_ALREADY_IN_USE,
        ]
    ),
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.EMAIL_CODE_INVALID,
            UnauthorizedErrorCodes.EMAIL_CODE_BLOCKED,
            UnauthorizedErrorCodes.EMAIL_CODE_EXPIRED,
            UnauthorizedErrorCodes.EMAIL_CODE_VALIDATED
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.EMAIL_CODE_CHECKING_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [InternalErrorCodes.CREATE_AUTH_ERROR,
         InternalErrorCodes.VALIDATE_EMAIL_CODE_INTERNAL_ERROR]
    )
}


update_password = {
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.INVALID_USER_CREDENTIALS
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.AUTH_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [InternalErrorCodes.UPDATE_PASSWORD_ERROR]
    )
}


reset_password = {
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.INVALID_USER_CREDENTIALS,
            UnauthorizedErrorCodes.EMAIL_CODE_INVALID,
            UnauthorizedErrorCodes.EMAIL_CODE_BLOCKED,
            UnauthorizedErrorCodes.EMAIL_CODE_EXPIRED,
            UnauthorizedErrorCodes.EMAIL_CODE_VALIDATED
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.AUTH_NOT_FOUND,
            NotFoundErrorCodes.EMAIL_CODE_CHECKING_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [InternalErrorCodes.RESET_PASSWORD_ERROR,
         InternalErrorCodes.VALIDATE_EMAIL_CODE_INTERNAL_ERROR]
    )
}


login = {
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.INVALID_USER_CREDENTIALS
        ]
    ),
    500: build_doc_errors_response(
        [InternalErrorCodes.LOGIN_INTERNAL_ERROR]
    )
}

send_email_create_auth_code = {
    400: build_doc_errors_response(
        [BadRequestErrorCode.EMAIL_ALREADY_IN_USE,
         BadRequestErrorCode.SEND_EMAIL_CODE_DISABLED]
    ),
    500: build_doc_errors_response(
        [InternalErrorCodes.SEND_EMAIL_CREATE_AUTH_CODE_ERROR,
         InternalErrorCodes.SEND_EMAIL_VERIFICATION_CODE_ERROR,
         InfraErrorCodes.RENDER_TEMPLATE_ERROR,
         InternalErrorCodes.CANNOT_PERSIST_EMAIL_CODE_ERROR,
         InfraErrorCodes.SEND_EMAIL_ERROR]
    )
}


send_email_forget_password = {
    400: build_doc_errors_response(
         [BadRequestErrorCode.SEND_EMAIL_CODE_DISABLED]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.AUTH_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [InternalErrorCodes.SEND_EMAIL_FORGET_PASSWORD_CODE_ERROR,
         InternalErrorCodes.SEND_EMAIL_VERIFICATION_CODE_ERROR,
         InfraErrorCodes.RENDER_TEMPLATE_ERROR,
         InternalErrorCodes.CANNOT_PERSIST_EMAIL_CODE_ERROR,
         InfraErrorCodes.SEND_EMAIL_ERROR]
    )
}

