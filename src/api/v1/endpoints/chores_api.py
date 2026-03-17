
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src.api.v1.dependencies.chores_dependencies import (
    assign_chore_to_me_use_case,
    complete_chore_use_case,
    list_today_chores_use_case,
    list_all_chores_use_case,
    create_chore_use_case,
    get_chore_use_case,
    update_chore_use_case,
    delete_chore_use_case,
    remove_assign_chore_to_me_use_case,
)
from src.api.v1.dependencies.shared_dependencies import get_current_user_entity
from src.api.v1.docs.errors import chores_error_docs
from src.api.v1.requests.chores.create_chore_request import CreateChoreRequest
from src.api.v1.requests.chores.get_chores_filtered_request import (
    GetChoresFilteredRequest,
)
from src.api.v1.requests.chores.update_chore_request import UpdateChoreRequest
from src.api.v1.responses.chores.chore_response import ChoreResponse
from src.api.v1.responses.chores.chores_paginated_response import (
    ChoresPaginatedResponse,
)
from src.application.usecases.chores.assign_chore_to_me_use_case import AssignChoreToMeUseCase
from src.application.usecases.chores.complete_chore_use_case import CompleteChoreUseCase
from src.application.usecases.chores.create_chore_use_case import CreateChoreUseCase
from src.application.usecases.chores.delete_chore_use_case import DeleteChoreUseCase
from src.application.usecases.chores.get_chore_use_case import GetChoreUseCase
from src.application.usecases.chores.list_all_chores_use_case import ListAllChoresUseCase
from src.application.usecases.chores.list_today_chores_use_case import ListTodayChoresUseCase
from src.application.usecases.chores.remove_assign_chore_to_me_use_case import RemoveAssignChoreToMeUseCase
from src.application.usecases.chores.update_chore_use_case import UpdateChoreUseCase
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.infra.decorators.logger import request_logging

router = APIRouter(prefix="/family/chores")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[ChoreResponse],
    responses=chores_error_docs.list_today_chores,
)
@request_logging
def list_today_chores(
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[ListTodayChoresUseCase, Depends(list_today_chores_use_case)],
) -> list[ChoreResponse]:
    return use_case.execute(family_id=user.family_id)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=ChoresPaginatedResponse,
    responses=chores_error_docs.list_all_chores,
)
@request_logging
def list_all_chores(
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[ListAllChoresUseCase, Depends(list_all_chores_use_case)],
    request: Annotated[GetChoresFilteredRequest, Depends()]
) -> ChoresPaginatedResponse:
    return use_case.execute(family_id=user.family_id, request=request)


@router.post(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=chores_error_docs.create_chore,
)
@request_logging
def create_chore(
    current_user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    request: CreateChoreRequest,
    use_case: Annotated[CreateChoreUseCase, Depends(create_chore_use_case)],
) -> Response:
    use_case.execute(
        request=request,
        current_user=current_user,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{chore_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=ChoreResponse,
    responses=chores_error_docs.get_chore,
)
@request_logging
def get_chore(
    chore_id: int,
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[GetChoreUseCase, Depends(get_chore_use_case)],
) -> ChoreResponse:
    return use_case.execute(chore_id=chore_id, family_id=user.family_id)


@router.put(
    "/{chore_id:int}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=chores_error_docs.update_chore,
)
@request_logging
def update_chore(
    chore_id: int,
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    request: UpdateChoreRequest,
    use_case: Annotated[UpdateChoreUseCase, Depends(update_chore_use_case)],
):
    use_case.execute(chore_id=chore_id, current_user=user, request=request)


@router.patch(
    "/{chore_id:int}/assign-to-me",
    status_code=status.HTTP_200_OK,
    response_model=ChoreResponse,
    responses=chores_error_docs.assign_chore_to_me,
)
@request_logging
def assign_chore_to_me(
    chore_id: int,
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[AssignChoreToMeUseCase, Depends(assign_chore_to_me_use_case)],
) -> ChoreResponse:
    return use_case.execute(chore_id=chore_id, current_user=user)


@router.patch(
    "/{chore_id:int}/remove-assign-to-me",
    status_code=status.HTTP_200_OK,
    response_model=ChoreResponse,
    responses=chores_error_docs.remove_assign_chore_to_me,
)
@request_logging
def remove_assign_chore_to_me(
    chore_id: int,
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[RemoveAssignChoreToMeUseCase, Depends(remove_assign_chore_to_me_use_case)],
) -> ChoreResponse:
    return use_case.execute(chore_id=chore_id, current_user=user)


@router.patch(
    "/{chore_id:int}/complete",
    status_code=status.HTTP_200_OK,
    response_model=ChoreResponse,
    responses=chores_error_docs.complete_chore,
)
@request_logging
def complete_chore(
    chore_id: int,
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[CompleteChoreUseCase, Depends(complete_chore_use_case)],
) -> ChoreResponse:
    return use_case.execute(chore_id=chore_id, current_user=user)


@router.delete(
    "/{chore_id:int}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=chores_error_docs.delete_chore,
)
@request_logging
def delete_chore(
    chore_id: int,
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[DeleteChoreUseCase, Depends(delete_chore_use_case)],
) -> None:
    use_case.execute(chore_id=chore_id, current_user=user)
