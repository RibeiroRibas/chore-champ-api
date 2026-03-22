from dataclasses import dataclass

from src.domain.schemas.dto.paginated_dto import PaginatedDto
from src.domain.schemas.entity.chore_entity import ChoreEntity


@dataclass
class GetPaginatedChoresDto(PaginatedDto[ChoreEntity]):
    pass