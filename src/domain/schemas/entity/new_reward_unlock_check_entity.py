from dataclasses import dataclass


@dataclass(frozen=True)
class NewRewardUnlockCheckEntity:
    """Resultado da leitura de pontos antes/depois de uma mutação e da deteção de desbloqueio."""

    available_points_before: int
    available_points_after: int
    new_reward_unlocked: bool
