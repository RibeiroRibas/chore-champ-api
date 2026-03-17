from dataclasses import dataclass

from src.application.schemas.paginated_dto import PaginatedDto
from src.domain.entities.chore_entity import ChoreEntity


@dataclass
class GetPaginatedChoresDto(PaginatedDto[ChoreEntity]):
    pass