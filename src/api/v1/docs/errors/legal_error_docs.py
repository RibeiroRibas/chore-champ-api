from src.api.v1.docs.models.api_error_docs import build_doc_errors_response
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes

get_privacy_policy = {
    500: build_doc_errors_response(
        [
            InternalErrorCodes.GET_PRIVACY_POLICY_ERROR,
        ]
    ),
}
