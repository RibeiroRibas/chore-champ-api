
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.api.v1.dependencies.chores_dependencies import (
    list_chores_use_case,
    create_chore_use_case,
    get_chore_use_case,
    update_chore_use_case,
    delete_chore_use_case,
)
from src.api.v1.dependencies.shared_dependencies import get_current_user_entity
from src.api.v1.docs.errors import chores_error_docs
from src.api.v1.requests.chores.create_chore_request import CreateChoreRequest
from src.api.v1.requests.chores.update_chore_request import UpdateChoreRequest
from src.api.v1.responses.chores.chore_response import ChoreResponse
from src.application.usecases.chores.create_chore_use_case import CreateChoreUseCase
from src.application.usecases.chores.delete_chore_use_case import DeleteChoreUseCase
from src.application.usecases.chores.get_chore_use_case import GetChoreUseCase
from src.application.usecases.chores.list_chores_use_case import ListChoresUseCase
from src.application.usecases.chores.update_chore_use_case import UpdateChoreUseCase
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.infra.decorators.logger import request_logging

router = APIRouter(prefix="/family/chores")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[ChoreResponse],
    responses=chores_error_docs.list_chores,
)
@request_logging
def list_chores(
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[ListChoresUseCase, Depends(list_chores_use_case)],
) -> list[ChoreResponse]:
    return use_case.execute(family_id=user.family_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ChoreResponse,
    responses=chores_error_docs.create_chore,
)
@request_logging
def create_chore(
    current_user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    request: CreateChoreRequest,
    use_case: Annotated[CreateChoreUseCase, Depends(create_chore_use_case)],
) -> ChoreResponse:
    return use_case.execute(
        request=request,
        current_user=current_user,
    )


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
    status_code=status.HTTP_200_OK,
    response_model=ChoreResponse,
    responses=chores_error_docs.update_chore,
)
@request_logging
def update_chore(
    chore_id: int,
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    request: UpdateChoreRequest,
    use_case: Annotated[UpdateChoreUseCase, Depends(update_chore_use_case)],
) -> ChoreResponse:
    return use_case.execute(chore_id=chore_id, current_user=user, request=request)


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
    use_case.execute(chore_id=chore_id, family_id=user.family_id)
