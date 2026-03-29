from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.api.v1.dependencies.legal_dependencies import get_privacy_policy_use_case
from src.api.v1.docs.errors import legal_error_docs
from src.api.v1.responses.legal.privacy_policy_response import PrivacyPolicyResponse
from src.application.usecases.legal.get_privacy_policy_use_case import (
    GetPrivacyPolicyUseCase,
)
from src.infra.decorators.logger import request_logging

router = APIRouter(prefix="/legal")


@router.get(
    "/privacy-policy",
    status_code=status.HTTP_200_OK,
    response_model=PrivacyPolicyResponse,
    responses=legal_error_docs.get_privacy_policy,
)
@request_logging
def get_privacy_policy(
    use_case: Annotated[
        GetPrivacyPolicyUseCase,
        Depends(get_privacy_policy_use_case),
    ],
) -> PrivacyPolicyResponse:
    return use_case.call()
