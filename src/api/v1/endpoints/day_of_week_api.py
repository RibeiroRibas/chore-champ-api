from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from src.api.v1.dependencies.day_of_week_dependencies import list_days_of_week_use_case
from src.api.v1.dependencies.shared_dependencies import get_current_user_entity
from src.api.v1.responses.days_of_week.day_of_week_response import DayOfWeekResponse
from src.application.usecases.days_of_week.list_days_of_week_use_case import ListDaysOfWeekUseCase
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.infra.decorators.logger import request_logging

router = APIRouter(prefix="/days-of-week")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[DayOfWeekResponse],
    summary="Listar dias da semana",
    description="Retorna a lista de dias da semana com id e nome (1=Segunda .. 7=Domingo).",
)
@request_logging
def list_days_of_week(
    _user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[ListDaysOfWeekUseCase, Depends(list_days_of_week_use_case)],
) -> list[DayOfWeekResponse]:
    return use_case.execute()
