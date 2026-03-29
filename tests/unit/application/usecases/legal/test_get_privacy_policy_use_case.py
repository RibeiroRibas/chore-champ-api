import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.application.usecases.legal.get_privacy_policy_use_case import (
    GetPrivacyPolicyUseCase,
)
from src.domain.errors.internal_error import InternalError


class TestGetPrivacyPolicyUseCase(unittest.TestCase):
    def test_call_returns_file_content(self):
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".md",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            tmp.write("# Title\n\nbody")
            path = Path(tmp.name)
        try:
            use_case = GetPrivacyPolicyUseCase(policy_file_path=path)
            result = use_case.call()
            self.assertEqual(result.content, "# Title\n\nbody")
        finally:
            path.unlink(missing_ok=True)

    def test_call_raises_internal_error_when_path_is_not_file(self):
        use_case = GetPrivacyPolicyUseCase(
            policy_file_path=Path("/nonexistent/privacy_policy.md"),
        )
        with self.assertRaises(InternalError):
            use_case.call()

    def test_call_raises_internal_error_when_read_text_fails(self):
        with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            tmp.write("ok")
            path = Path(tmp.name)
        try:
            use_case = GetPrivacyPolicyUseCase(policy_file_path=path)
            with patch.object(Path, "read_text", side_effect=OSError("denied")):
                with self.assertRaises(InternalError):
                    use_case.call()
        finally:
            path.unlink(missing_ok=True)
