from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.api.middlewares.access_token_middleware import get_current_auth_id
from src.api.v1.dependencies.users_dependencies import create_current_user_and_family_use_case, update_current_user_use_case, \
    get_current_user_use_case
from src.api.v1.docs.errors import users_error_docs
from src.api.v1.requests.users.create_current_user_request import CreateCurrentUserRequest
from src.api.v1.requests.users.update_current_user_request import UpdateCurrentUserRequest
from src.api.v1.responses.users.current_user_response import CurrentUserResponse
from src.application.usecases.users.create_current_user_and_family_use_case import CreateCurrentUserAndFamilyUseCase
from src.application.usecases.users.get_current_user_use_case import GetCurrentUserUseCase
from src.application.usecases.users.update_current_user_use_case import UpdateCurrentUserUseCase
from src.infra.decorators.logger import request_logging

router = APIRouter(prefix="/users")

@router.post("/current-and-family",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=users_error_docs.create_current_user
)
@request_logging
def create_current_user_and_family(use_case: Annotated[CreateCurrentUserAndFamilyUseCase, Depends(create_current_user_and_family_use_case)],
                                    request: CreateCurrentUserRequest, current_auth_id: Annotated[int, Depends(get_current_auth_id)]):
    return use_case.execute(request=request, auth_id=current_auth_id)


@router.put("/current",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=users_error_docs.update_current_user
)
@request_logging
def update_current_user(use_case: Annotated[UpdateCurrentUserUseCase, Depends(update_current_user_use_case)],
        request: UpdateCurrentUserRequest, current_auth_id: Annotated[int, Depends(get_current_auth_id)]):
    return use_case.execute(request=request, auth_id=current_auth_id)


@router.get("/current",
    status_code=status.HTTP_200_OK,
    response_model=CurrentUserResponse,
    responses=users_error_docs.get_current_user
)
@request_logging
def get_current_user(use_case: Annotated[GetCurrentUserUseCase, Depends(get_current_user_use_case)],
                     current_auth_id: Annotated[int, Depends(get_current_auth_id)]) -> CurrentUserResponse:
    return use_case.execute(auth_id=current_auth_id)
