from typing import Annotated

from fastapi import BackgroundTasks, Depends, APIRouter
from starlette import status

from src.api.v1.dependencies.family_members_dependencies import list_family_members_use_case, \
    create_family_member_use_case, get_family_member_use_case, update_family_member_use_case, \
    delete_family_member_use_case, resend_family_member_password_use_case
from src.api.v1.dependencies.shared_dependencies import has_permission_admin_use_case, get_current_user_entity
from src.api.v1.docs.errors import family_members_error_docs
from src.api.v1.requests.users.create_family_member_request import CreateFamilyMemberRequest
from src.api.v1.requests.users.update_family_member_request import UpdateFamilyMemberRequest
from src.api.v1.responses.users.family_member_response import FamilyMemberResponse
from src.application.usecases.family.create_family_member_use_case import CreateFamilyMemberUseCase
from src.application.usecases.family.delete_family_member_use_case import DeleteFamilyMemberUseCase
from src.application.usecases.family.get_family_member_use_case import GetFamilyMemberUseCase
from src.application.usecases.family.list_family_members_use_case import ListFamilyMembersUseCase
from src.application.usecases.family.resend_family_member_password_use_case import (
    ResendFamilyMemberPasswordUseCase,
)
from src.application.usecases.family.update_family_member_use_case import UpdateFamilyMemberUseCase
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.infra.decorators.logger import request_logging
from src.infra.services.send_email_service import send_temp_password

router = APIRouter(prefix='/family/users')


def _schedule_send_temp_password(
    background_tasks: BackgroundTasks,
    email: str,
    temp_password: str,
) -> None:
    background_tasks.add_task(send_temp_password, email=email, temp_password=temp_password)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[FamilyMemberResponse],
    responses=family_members_error_docs.list_family_members,
)
@request_logging
def list_family_members(
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[ListFamilyMembersUseCase, Depends(list_family_members_use_case)],
) -> list[FamilyMemberResponse]:
    return use_case.execute(family_id=user.family_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=FamilyMemberResponse,
    responses=family_members_error_docs.create_family_member,
)
@request_logging
def create_family_member(
    user: Annotated[CurrentUserEntity, Depends(has_permission_admin_use_case)],
    request: CreateFamilyMemberRequest,
    background_tasks: BackgroundTasks,
    use_case: Annotated[CreateFamilyMemberUseCase, Depends(create_family_member_use_case)],
) -> FamilyMemberResponse:

    def send_later(email: str, temp_password: str) -> None:
        _schedule_send_temp_password(background_tasks, email, temp_password)

    return use_case.execute(
        request=request,
        family_id=user.family_id,
        send_email_async=send_later,
    )


@router.get(
    "/{user_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=FamilyMemberResponse,
    responses=family_members_error_docs.get_family_member,
)
@request_logging
def get_family_member(
    user_id: int,
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[GetFamilyMemberUseCase, Depends(get_family_member_use_case)],
) -> FamilyMemberResponse:
    return use_case.execute(user_id=user_id, family_id=user.family_id)


@router.put(
    "/{user_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=FamilyMemberResponse,
    responses=family_members_error_docs.update_family_member,
)
@request_logging
def update_family_member(
    user_id: int,
    user: Annotated[CurrentUserEntity, Depends(has_permission_admin_use_case)],
    request: UpdateFamilyMemberRequest,
    use_case: Annotated[UpdateFamilyMemberUseCase, Depends(update_family_member_use_case)],
) -> FamilyMemberResponse:
    return use_case.execute(user_id=user_id, family_id=user.family_id, request=request)


@router.delete(
    "/{user_id:int}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=family_members_error_docs.delete_family_member,
)
@request_logging
def delete_family_member(
    user_id: int,
    user: Annotated[CurrentUserEntity, Depends(has_permission_admin_use_case)],
    use_case: Annotated[DeleteFamilyMemberUseCase, Depends(delete_family_member_use_case)],
) -> None:
    use_case.execute(user_id=user_id, family_id=user.family_id)


@router.post(
    "/{user_id:int}/resend-password",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=family_members_error_docs.resend_family_member_password,
)
@request_logging
def resend_family_member_password(
    user_id: int,
    user: Annotated[CurrentUserEntity, Depends(has_permission_admin_use_case)],
    background_tasks: BackgroundTasks,
    use_case: Annotated[
        ResendFamilyMemberPasswordUseCase, Depends(resend_family_member_password_use_case)
    ],
) -> None:

    def send_later(email: str, temp_password: str) -> None:
        _schedule_send_temp_password(background_tasks, email, temp_password)

    use_case.execute(
        user_id=user_id,
        family_id=user.family_id,
        send_email_async=send_later,
    )