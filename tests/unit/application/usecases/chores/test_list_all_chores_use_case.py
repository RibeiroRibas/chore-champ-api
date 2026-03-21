import unittest
from unittest.mock import MagicMock

from src.api.v1.requests.chores.get_chores_filtered_request import (
    GetChoresFilteredRequest,
)
from src.application.schemas.paginated_dto import PaginatedDto
from src.domain.entities.chore_entity import ChoreEntity
from src.domain.errors.internal_error import InternalError
from src.application.usecases.chores.list_all_chores_use_case import (
    ListAllChoresUseCase,
)


class TestListAllChoresUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.use_case = ListAllChoresUseCase(chore_repository=self.mock_repo)

    def test_execute_returns_paginated_response(self):
        chore = ChoreEntity(
            chore_id=1,
            family_id=1,
            title="Tarefa",
            emoji="🧹",
            points=5,
            assigned_to_user_id=None,
            created_by_user_id=1,
            completed=False,
        )
        paginated = PaginatedDto(
            items=[chore],
            total_items=1,
            page=1,
            page_size=20,
            total_pages=1,
        )
        self.mock_repo.find_paginated.return_value = paginated
        request = GetChoresFilteredRequest()
        result = self.use_case.execute(family_id=1, request=request)
        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.items[0].id, 1)
        self.assertEqual(result.total_items, 1)
        self.assertEqual(result.page, 1)
        self.mock_repo.find_paginated.assert_called_once()

    def test_execute_returns_empty_page_when_no_results(self):
        paginated = PaginatedDto(
            items=[],
            total_items=0,
            page=1,
            page_size=20,
            total_pages=0,
        )
        self.mock_repo.find_paginated.return_value = paginated
        request = GetChoresFilteredRequest()
        result = self.use_case.execute(family_id=1, request=request)
        self.assertEqual(result.items, [])
        self.assertEqual(result.total_items, 0)

    def test_execute_passes_filters_to_repository(self):
        paginated = PaginatedDto(
            items=[],
            total_items=0,
            page=2,
            page_size=10,
            total_pages=0,
        )
        self.mock_repo.find_paginated.return_value = paginated
        request = GetChoresFilteredRequest(
            completed=True,
            is_recurring=True,
            title="test",
            assigned_to_user_id=5,
            page=2,
            page_size=10,
        )
        self.use_case.execute(family_id=1, request=request)
        call_kwargs = self.mock_repo.find_paginated.call_args.kwargs
        self.assertEqual(call_kwargs["family_id"], 1)
        dto = call_kwargs["dto"]
        self.assertEqual(dto.completed, True)
        self.assertEqual(dto.is_recurring, True)
        self.assertEqual(dto.title, "test")
        self.assertEqual(dto.assigned_to_user_id, 5)
        self.assertEqual(dto.page, 2)
        self.assertEqual(dto.page_size, 10)

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError

        self.mock_repo.find_paginated.side_effect = BadRequestError(code=400)
        with self.assertRaises(BadRequestError):
            self.use_case.execute(
                family_id=1,
                request=GetChoresFilteredRequest(),
            )

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_repo.find_paginated.side_effect = RuntimeError("DB error")
        with self.assertRaises(InternalError):
            self.use_case.execute(
                family_id=1,
                request=GetChoresFilteredRequest(),
            )
