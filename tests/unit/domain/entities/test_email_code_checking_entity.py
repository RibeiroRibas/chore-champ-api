import unittest
from datetime import datetime, timedelta

from src.domain.entities.email_code_checking_entity import EmailCodeCheckingEntity
from src.domain.errors.unauthorized_error import UnauthorizedError


class TestEmailCodeCheckingEntity(unittest.TestCase):
    def _entity(
        self,
        code: int = 123456,
        is_blocked: bool = False,
        validated: bool = False,
        validation_attempts: int = 0,
        created_at: datetime | None = None,
    ) -> EmailCodeCheckingEntity:
        if created_at is None:
            created_at = datetime.now()
        return EmailCodeCheckingEntity(
            id=1,
            email="test@example.com",
            code=code,
            is_blocked=is_blocked,
            validated=validated,
            validation_attempts=validation_attempts,
            created_at=created_at,
        )

    def test_validate_succeeds_when_code_matches(self):
        entity = self._entity(code=123456)
        entity.validate(123456)
        self.assertTrue(entity.validated)

    def test_validate_raises_when_already_validated(self):
        entity = self._entity(validated=True)
        with self.assertRaises(UnauthorizedError):
            entity.validate(123456)

    def test_validate_raises_when_expired(self):
        expired_at = datetime.now() - timedelta(minutes=20)
        entity = self._entity(created_at=expired_at, code=123456)
        with self.assertRaises(UnauthorizedError):
            entity.validate(123456)

    def test_validate_raises_when_blocked(self):
        entity = self._entity(is_blocked=True, code=123456)
        with self.assertRaises(UnauthorizedError):
            entity.validate(123456)

    def test_validate_does_not_set_validated_when_code_wrong(self):
        entity = self._entity(code=123456)
        entity.validate(999999)  # wrong code - entity does not raise
        self.assertFalse(entity.validated)

    def test_update_attempts_increments_attempts(self):
        entity = self._entity(validation_attempts=1)
        entity.update_attempts()
        self.assertEqual(entity.validation_attempts, 2)

    def test_update_attempts_blocks_after_max_attempts(self):
        entity = self._entity(validation_attempts=2)  # 3rd attempt will block
        entity.update_attempts()
        self.assertEqual(entity.validation_attempts, 3)
        self.assertTrue(entity.is_blocked)

    def test_update_attempts_does_not_block_before_max(self):
        entity = self._entity(validation_attempts=1)
        entity.update_attempts()
        self.assertFalse(entity.is_blocked)
