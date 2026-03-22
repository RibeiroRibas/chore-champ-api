from src.api.v1.responses.days_of_week.day_of_week_response import DayOfWeekResponse
from src.domain.schemas.entity.day_of_week_entity import DayOfWeekEntity
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.repositories.day_of_week_repository import DayOfWeekRepository


class ListDaysOfWeekUseCase:
    def __init__(self, day_of_week_repository: DayOfWeekRepository):
        self.day_of_week_repository = day_of_week_repository

    def execute(self) -> list[DayOfWeekResponse]:
        try:
            entities: list[DayOfWeekEntity] = self.day_of_week_repository.find_all()
            return [DayOfWeekResponse.from_entity(e) for e in entities]
        except Exception:
            raise InternalError(code=InternalErrorCodes.LIST_DAYS_OF_WEEK_ERROR.code())
