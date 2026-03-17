from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.usecases.days_of_week.list_days_of_week_use_case import ListDaysOfWeekUseCase
from src.infra.database.database import get_db
from src.repositories.day_of_week_repository import DayOfWeekRepository


def list_days_of_week_use_case(db: Session = Depends(get_db)) -> ListDaysOfWeekUseCase:
    return ListDaysOfWeekUseCase(
        day_of_week_repository=DayOfWeekRepository(db_session=db),
    )
