from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.usecases.auth.create_auth_use_case import CreateAuthUseCase
from src.application.usecases.auth.login_use_case import LoginUseCase
from src.application.usecases.auth.reset_password_use_case import ResetPasswordUseCase
from src.application.usecases.auth.send_email_create_auth_code_use_case import SendEmailCreateAuthCodeUseCase
from src.application.usecases.auth.send_email_forget_password_code_use_case import SendEmailForgetPasswordCodeUseCase
from src.application.usecases.auth.send_email_verification_code_use_case import SendEmailVerificationCodeUseCase
from src.application.usecases.auth.update_password_use_case import UpdatePasswordUseCase
from src.application.usecases.auth.validate_email_code_checking_use_case import ValidateEmailCodeCheckingUseCase
from src.infra.database.database import get_db
from src.infra.services.jwt_service import JWTService
from src.repositories.auth_repository import AuthRepository
from src.repositories.email_code_checking_repository import EmailCodeCheckingRepository


def create_auth_use_case(db: Session = Depends(get_db)) -> CreateAuthUseCase:
    auth_repository = AuthRepository(db_session=db)
    email_code_checking_repository= EmailCodeCheckingRepository(db_session=db)
    validate_email_code_use_case = ValidateEmailCodeCheckingUseCase(email_code_checking_repository=email_code_checking_repository)
    return CreateAuthUseCase(auth_repository=auth_repository, validate_email_code_use_case=validate_email_code_use_case)

def login_use_case(db: Session = Depends(get_db)) -> LoginUseCase:
    auth_repository = AuthRepository(db_session=db)
    jwt_service = JWTService()
    return LoginUseCase(auth_repository=auth_repository, jwt_service=jwt_service)

def send_email_create_auth_code_use_case(db: Session = Depends(get_db)) -> SendEmailCreateAuthCodeUseCase:
    auth_repository = AuthRepository(db_session=db)
    email_code_checking_repository = EmailCodeCheckingRepository(db_session=db)
    send_email_verification_code_use_case = SendEmailVerificationCodeUseCase(email_code_checking_repository=email_code_checking_repository)
    return SendEmailCreateAuthCodeUseCase(auth_repository=auth_repository,
                                          send_email_verification_code_use_case=send_email_verification_code_use_case)

def update_password_use_case(db: Session = Depends(get_db)) -> UpdatePasswordUseCase:
    auth_repository = AuthRepository(db_session=db)
    return UpdatePasswordUseCase(auth_repository=auth_repository)

def send_email_forget_password_code_use_case(db: Session = Depends(get_db)) -> SendEmailForgetPasswordCodeUseCase:
    auth_repository = AuthRepository(db_session=db)
    email_code_checking_repository = EmailCodeCheckingRepository(db_session=db)
    send_email_verification_code_use_case = SendEmailVerificationCodeUseCase(email_code_checking_repository=email_code_checking_repository)
    return SendEmailForgetPasswordCodeUseCase(auth_repository=auth_repository,
                                          send_email_verification_code_use_case=send_email_verification_code_use_case)

def reset_password_use_case(db: Session = Depends(get_db)) -> ResetPasswordUseCase:
    auth_repository = AuthRepository(db_session=db)
    email_code_checking_repository= EmailCodeCheckingRepository(db_session=db)
    validate_email_code_use_case = ValidateEmailCodeCheckingUseCase(email_code_checking_repository=email_code_checking_repository)
    return ResetPasswordUseCase(auth_repository=auth_repository, validate_email_code_use_case=validate_email_code_use_case)