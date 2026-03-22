import unittest
from unittest.mock import MagicMock

from src.api.v1.requests.chores.create_chore_request import CreateChoreRequest
from src.application.schemas.chores.create_chore_dto import CreateChoreDTO
from src.application.usecases.chores.create_chore_use_case import CreateChoreUseCase
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.enums.user_role_enum import UserRoleEnum
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.internal_error import InternalError


class TestCreateChoreUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_service = MagicMock()
        self.use_case = CreateChoreUseCase(
            create_chore_service=self.mock_service,
        )

    def _admin(self) -> CurrentUserEntity:
        return CurrentUserEntity(
            user_id=1,
            auth_id=10,
            role_id=UserRoleEnum.ADMIN.value[0],
            family_id=2,
        )

    def test_call_raises_bad_request_when_recurring_without_days(self):
        request = CreateChoreRequest(
            title="T",
            points=5,
            is_recurring=True,
            recurrence_day_ids=None,
        )
        with self.assertRaises(BadRequestError):
            self.use_case.call(request=request, current_user=self._admin())

    def test_call_invokes_service_once_when_no_assignees(self):
        request = CreateChoreRequest(
            title="T",
            points=5,
            assigned_to_user_ids=[],
        )
        self.mock_service.execute.return_value = False
        result = self.use_case.call(request=request, current_user=self._admin())
        self.assertFalse(result)
        self.assertEqual(self.mock_service.execute.call_count, 1)
        call_dto = self.mock_service.execute.call_args[0][0]
        self.assertIsInstance(call_dto, CreateChoreDTO)
        self.assertIsNone(call_dto.assigned_to_user_id)

    def test_call_invokes_service_twice_when_two_assignees(self):
        request = CreateChoreRequest(
            title="T",
            points=5,
            assigned_to_user_ids=[3, 4],
        )
        self.mock_service.execute.return_value = False
        self.use_case.call(request=request, current_user=self._admin())
        self.assertEqual(self.mock_service.execute.call_count, 2)
        first_id = self.mock_service.execute.call_args_list[0][0][0].assigned_to_user_id
        second_id = self.mock_service.execute.call_args_list[1][0][0].assigned_to_user_id
        self.assertEqual(first_id, 3)
        self.assertEqual(second_id, 4)

    def test_call_combines_reward_unlock_with_or(self):
        request = CreateChoreRequest(
            title="T",
            points=5,
            assigned_to_user_ids=[1, 2],
        )
        self.mock_service.execute.side_effect = [
            False,
            True,
        ]
        result = self.use_case.call(request=request, current_user=self._admin())
        self.assertTrue(result)

    def test_call_reraises_base_error(self):
        request = CreateChoreRequest(title="T", points=5)
        self.mock_service.execute.side_effect = BadRequestError(code=400)
        with self.assertRaises(BadRequestError):
            self.use_case.call(request=request, current_user=self._admin())

    def test_call_raises_internal_error_on_unexpected_exception(self):
        request = CreateChoreRequest(title="T", points=5)
        self.mock_service.execute.side_effect = RuntimeError("x")
        with self.assertRaises(InternalError):
            self.use_case.call(request=request, current_user=self._admin())
