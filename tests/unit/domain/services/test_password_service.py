import unittest

from src.domain.services import password_service


class TestPasswordService(unittest.TestCase):
    def test_hash_password_returns_non_empty_string(self):
        hashed = password_service.hash_password("secret")
        self.assertIsInstance(hashed, str)
        self.assertGreater(len(hashed), 0)
        self.assertNotEqual(hashed, "secret")

    def test_hash_password_produces_different_hashes_for_same_input(self):
        h1 = password_service.hash_password("secret")
        h2 = password_service.hash_password("secret")
        self.assertNotEqual(h1, h2)

    def test_verify_password_returns_true_when_password_matches(self):
        plain = "secret123"
        hashed = password_service.hash_password(plain)
        self.assertTrue(password_service.verify_password(plain, hashed))

    def test_verify_password_returns_false_when_password_does_not_match(self):
        hashed = password_service.hash_password("secret")
        self.assertFalse(password_service.verify_password("wrong", hashed))

    def test_verify_password_returns_false_for_empty_plain(self):
        hashed = password_service.hash_password("secret")
        self.assertFalse(password_service.verify_password("", hashed))

    def test_generate_temp_password_returns_correct_length(self):
        pwd = password_service.generate_temp_password(length=6)
        self.assertEqual(len(pwd), 6)
        pwd10 = password_service.generate_temp_password(length=10)
        self.assertEqual(len(pwd10), 10)

    def test_generate_temp_password_returns_only_digits(self):
        pwd = password_service.generate_temp_password(length=8)
        self.assertTrue(pwd.isdigit())

    def test_generate_temp_password_default_length_is_six(self):
        pwd = password_service.generate_temp_password()
        self.assertEqual(len(pwd), 6)
