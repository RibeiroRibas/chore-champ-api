from src.api.v1.docs.models.api_error_docs import build_doc_errors_response
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.codes.unauthorized_error_codes import UnauthorizedErrorCodes
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes


get_family_achievements = {
    401: build_doc_errors_response(
        [
            UnauthorizedErrorCodes.INSUFFICIENT_PERMISSIONS,
        ]
    ),
    404: build_doc_errors_response(
        [
            NotFoundErrorCodes.CURRENT_USER_NOT_FOUND,
        ]
    ),
    500: build_doc_errors_response(
        [
            InternalErrorCodes.GET_FAMILY_ACHIEVEMENTS_ERROR,
        ]
    ),
}

