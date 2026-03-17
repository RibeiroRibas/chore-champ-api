from dataclasses import dataclass

from src.application.schemas.common_filters_dto import CommonFiltersDto


@dataclass
class GetChoresFilteredDto(CommonFiltersDto):
    completed: bool | None
    is_recurring: bool | None
    title: str | None
    assigned_to_user_id: int | None