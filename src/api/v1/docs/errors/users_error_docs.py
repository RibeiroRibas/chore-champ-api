from src.api.v1.docs.models.api_error_docs import build_doc_errors_response
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes

create_current_user = {
    400: build_doc_errors_response(
        [
            BadRequestErrorCode.USER_ALREADY_REGISTERED_FOR_THIS_AUTH,
        ]
    ),
    500: build_doc_errors_response(
        [InternalErrorCodes.CREATE_CURRENT_USER_ERROR]
    )
}


get_current_user = {
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.USER_NOT_FOUND,
            NotFoundErrorCodes.FAMILY_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [InternalErrorCodes.GET_CURRENT_USER_ERROR]
    )
}

update_current_user = {
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.USER_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [InternalErrorCodes.UPDATE_CURRENT_USER_ERROR]
    )
}
