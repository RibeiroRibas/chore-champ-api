import unittest
from unittest.mock import MagicMock

from src.domain.schemas.dto.users.add_user_points_dto import AddUserPointsDTO
from src.domain.schemas.entity.points_entity import PointsEntity
from src.domain.errors.internal_error import InternalError
from src.domain.services.save_user_points_service import SaveUserPointsService


class TestSaveUserPointsService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = SaveUserPointsService(
            user_points_repository=self.mock_repo
        )

    def test_execute_inserts_when_user_has_no_points(self):
        self.mock_repo.find_by_user_id.return_value = None
        dto = AddUserPointsDTO(user_id=1, points=10, family_id=2)
        self.service.execute(dto=dto)
        self.mock_repo.find_by_user_id.assert_called_once_with(user_id=1)
        self.mock_repo.insert.assert_called_once()
        insert_dto = self.mock_repo.insert.call_args.kwargs["dto"]
        self.assertEqual(insert_dto.user_id, 1)
        self.assertEqual(insert_dto.family_id, 2)
        self.assertEqual(insert_dto.total_points, 10)

    def test_execute_updates_when_user_has_existing_points(self):
        existing = PointsEntity(
            id=1,
            total_points=50,
            user_id=1,
            points_redeemed=0,
            family_id=2,
        )
        self.mock_repo.find_by_user_id.return_value = existing
        dto = AddUserPointsDTO(user_id=1, points=10, family_id=2)
        self.service.execute(dto=dto)
        self.mock_repo.update_total_points.assert_called_once_with(
            user_id=1,
            total_points=60,
        )

    def test_execute_reraises_base_error(self):
        from src.domain.errors.bad_request_error import BadRequestError
        self.mock_repo.find_by_user_id.side_effect = BadRequestError(code=400)
        dto = AddUserPointsDTO(user_id=1, points=10, family_id=2)
        with self.assertRaises(BadRequestError):
            self.service.execute(dto=dto)

    def test_execute_raises_internal_error_on_unexpected_exception(self):
        self.mock_repo.find_by_user_id.side_effect = RuntimeError("DB error")
        dto = AddUserPointsDTO(user_id=1, points=10, family_id=2)
        with self.assertRaises(InternalError):
            self.service.execute(dto=dto)
