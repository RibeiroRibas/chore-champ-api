from src.domain.errors.models.base_error_code import BaseErrorCode
from src.domain.errors.models.error_model import ErrorModel


def __build_doc_description(errors: list[BaseErrorCode]) -> str:
    description: str = ""
    for error in errors:
        if description == "":
            description = f"{error.code()}: {error.message()}"
        else:
            description = f"{description}   |   {error.code()}: {error.message()}"
    return description


def build_doc_errors_response(errors: list[BaseErrorCode]):
    return {
        "description": __build_doc_description(errors),
        "model": ErrorModel
    }