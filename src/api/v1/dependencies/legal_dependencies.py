from src.application.usecases.legal.get_privacy_policy_use_case import (
    GetPrivacyPolicyUseCase,
)


def get_privacy_policy_use_case() -> GetPrivacyPolicyUseCase:
    return GetPrivacyPolicyUseCase()
