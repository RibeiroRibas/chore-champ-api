from pydantic import BaseModel, Field


class ChoreRewardUnlockResponse(BaseModel):
    new_reward_unlocked: bool = Field(
        ...,
        description="True se pelo menos uma recompensa da família ficou desbloqueada para o utilizador após os pontos ganhos.",
        examples=[False],
    )
