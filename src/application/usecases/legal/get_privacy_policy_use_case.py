from pathlib import Path

from src.api.v1.responses.legal.privacy_policy_response import PrivacyPolicyResponse
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging


class GetPrivacyPolicyUseCase:
    def __init__(self):
        src_root = Path(__file__).resolve().parents[3]
        self.__path = src_root / "infra" / "content" / "privacy_policy.md"

    @logging(show_args=True, show_return=True)
    def call(self) -> PrivacyPolicyResponse:
        try:
            return self.__read()
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.GET_PRIVACY_POLICY_ERROR.code())

    def __read(self) -> PrivacyPolicyResponse:
        if not self.__path.is_file():
            raise InternalError(code=InternalErrorCodes.GET_PRIVACY_POLICY_ERROR.code())
        text = self.__path.read_text(encoding="utf-8")
        return PrivacyPolicyResponse(content=text)
