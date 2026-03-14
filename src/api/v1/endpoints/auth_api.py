from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import EmailStr
from starlette import status

from src.api.middlewares.access_token_middleware import get_current_auth_id
from src.api.v1.dependencies.auth_dependencies import login_use_case, create_auth_use_case, \
    send_email_create_auth_code_use_case, update_password_use_case, reset_password_use_case, \
    send_email_forget_password_code_use_case, refresh_token_use_case
from src.api.v1.docs.errors import auth_error_docs
from src.api.v1.requests.auth.create_auth_request import CreateAuthRequest
from src.api.v1.requests.auth.login_request import LoginRequest
from src.api.v1.requests.auth.refresh_request import RefreshRequest
from src.api.v1.requests.auth.reset_password_request import ResetPasswordRequest
from src.api.v1.requests.auth.update_password_request import UpdatePasswordRequest
from src.api.v1.responses.auth.login_response import LoginResponse
from src.application.usecases.auth.create_auth_use_case import CreateAuthUseCase
from src.application.usecases.auth.login_use_case import LoginUseCase
from src.application.usecases.auth.refresh_token_use_case import RefreshTokenUseCase
from src.application.usecases.auth.reset_password_use_case import ResetPasswordUseCase
from src.application.usecases.auth.send_email_create_auth_code_use_case import SendEmailCreateAuthCodeUseCase
from src.application.usecases.auth.send_email_forget_password_code_use_case import SendEmailForgetPasswordCodeUseCase
from src.application.usecases.auth.update_password_use_case import UpdatePasswordUseCase
from src.infra.decorators.logger import request_logging

router = APIRouter(prefix="/auth")


@router.post("/login",
    status_code=status.HTTP_201_CREATED,
    response_model=LoginResponse,
    responses=auth_error_docs.login
)
@request_logging
def login(use_case: Annotated[LoginUseCase, Depends(login_use_case)], request: LoginRequest):
    return use_case.execute(username=request.email, password=request.password)


@router.post("/refresh",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    responses=auth_error_docs.refresh
)
@request_logging
def refresh(
    use_case: Annotated[RefreshTokenUseCase, Depends(refresh_token_use_case)],
    request: RefreshRequest,
):
    return use_case.execute(
        refresh_token=request.refresh_token,
        current_auth_id=request.current_auth_id,
    )


@router.post("/send-email-create-auth-code/{email}",
    status_code=status.HTTP_204_NO_CONTENT,
             responses=auth_error_docs.send_email_create_auth_code
)
@request_logging
def send_email_create_auth_code(
        use_case: Annotated[SendEmailCreateAuthCodeUseCase, Depends(send_email_create_auth_code_use_case)],
        email: EmailStr):
    return use_case.execute(email=email)


@router.post("",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=auth_error_docs.create_auth
)
@request_logging
def create(use_case: Annotated[CreateAuthUseCase, Depends(create_auth_use_case)], request: CreateAuthRequest):
    return use_case.execute(request=request)


@router.post("/send-email-forget-password-code/{email}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=auth_error_docs.send_email_forget_password
)
@request_logging
def send_email_forget_password_code(
        use_case: Annotated[SendEmailForgetPasswordCodeUseCase, Depends(send_email_forget_password_code_use_case)],
        email: EmailStr):
    return use_case.execute(email=email)


@router.patch("/reset-password",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=auth_error_docs.reset_password
)
@request_logging
def reset_password(use_case: Annotated[ResetPasswordUseCase, Depends(reset_password_use_case)],
                    request: ResetPasswordRequest):
    return use_case.execute(request=request)


@router.patch("/password",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=auth_error_docs.update_password
)
@request_logging
def update_password(use_case: Annotated[UpdatePasswordUseCase, Depends(update_password_use_case)],
                    request: UpdatePasswordRequest, current_auth_id: Annotated[int, Depends(get_current_auth_id)]):
    return use_case.execute(request=request, auth_id=current_auth_id)
