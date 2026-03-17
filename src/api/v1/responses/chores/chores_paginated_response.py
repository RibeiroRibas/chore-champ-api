from src.api.v1.responses.chores.chore_response import ChoreResponse
from src.api.v1.responses.paginated_response import PaginatedResponse


class ChoresPaginatedResponse(PaginatedResponse[ChoreResponse]):
    """Resposta paginada de tarefas."""
