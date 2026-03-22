import unittest

from src.domain.schemas.entity.points_entity import PointsEntity


class TestPointsEntity(unittest.TestCase):
    def test_available_points_returns_total_minus_redeemed(self):
        points = PointsEntity(
            id=1,
            total_points=100,
            user_id=1,
            points_redeemed=30,
            family_id=1,
        )
        self.assertEqual(points.available_points(), 70)

    def test_available_points_returns_zero_when_all_redeemed(self):
        points = PointsEntity(
            id=1,
            total_points=100,
            user_id=1,
            points_redeemed=100,
            family_id=1,
        )
        self.assertEqual(points.available_points(), 0)

    def test_available_points_returns_total_when_none_redeemed(self):
        points = PointsEntity(
            id=1,
            total_points=50,
            user_id=1,
            points_redeemed=0,
            family_id=1,
        )
        self.assertEqual(points.available_points(), 50)
