from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src.api.v1.dependencies.rewards_dependencies import (
    claim_reward_use_case,
    create_reward_use_case,
    delete_reward_use_case,
    get_reward_use_case,
    list_family_rewards_use_case,
    update_reward_use_case,
)
from src.api.v1.dependencies.shared_dependencies import (
    get_current_user_entity,
    has_permission_admin_use_case,
)
from src.api.v1.docs.errors import rewards_error_docs
from src.api.v1.requests.rewards.create_reward_request import CreateRewardRequest
from src.api.v1.requests.rewards.update_reward_request import UpdateRewardRequest
from src.api.v1.responses.rewards.reward_response import RewardResponse
from src.application.usecases.rewards.claim_reward_use_case import ClaimRewardUseCase
from src.application.usecases.rewards.create_reward_use_case import CreateRewardUseCase
from src.application.usecases.rewards.delete_reward_use_case import DeleteRewardUseCase
from src.application.usecases.rewards.get_reward_use_case import GetRewardUseCase
from src.application.usecases.rewards.list_family_rewards_use_case import ListFamilyRewardsUseCase
from src.application.usecases.rewards.update_reward_use_case import UpdateRewardUseCase
from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.infra.decorators.logger import request_logging

router = APIRouter(prefix="/family/rewards")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[RewardResponse],
    responses=rewards_error_docs.list_rewards,
)
@request_logging
def list_family_rewards(
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[ListFamilyRewardsUseCase, Depends(list_family_rewards_use_case)],
) -> list[RewardResponse]:
    return use_case.execute(user_id=user.user_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=RewardResponse,
    responses=rewards_error_docs.create_reward,
)
@request_logging
def create_reward(
    user: Annotated[CurrentUserEntity, Depends(has_permission_admin_use_case)],
    request: CreateRewardRequest,
    use_case: Annotated[CreateRewardUseCase, Depends(create_reward_use_case)],
) -> RewardResponse:
    return use_case.execute(request=request, user_id=user.user_id)


@router.get(
    "/{reward_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=RewardResponse,
    responses=rewards_error_docs.get_reward,
)
@request_logging
def get_reward(
    reward_id: int,
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[GetRewardUseCase, Depends(get_reward_use_case)],
) -> RewardResponse:
    return use_case.execute(reward_id=reward_id, user_id=user.user_id)


@router.put(
    "/{reward_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=RewardResponse,
    responses=rewards_error_docs.update_reward,
)
@request_logging
def update_reward(
    reward_id: int,
    user: Annotated[CurrentUserEntity, Depends(has_permission_admin_use_case)],
    request: UpdateRewardRequest,
    use_case: Annotated[UpdateRewardUseCase, Depends(update_reward_use_case)],
) -> RewardResponse:
    return use_case.execute(reward_id=reward_id, request=request, user_id=user.user_id)


@router.delete(
    "/{reward_id:int}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=rewards_error_docs.delete_reward,
)
@request_logging
def delete_reward(
    reward_id: int,
    _: Annotated[CurrentUserEntity, Depends(has_permission_admin_use_case)],
    use_case: Annotated[DeleteRewardUseCase, Depends(delete_reward_use_case)],
) -> Response:
    use_case.execute(reward_id=reward_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{reward_id:int}/claim",
    status_code=status.HTTP_200_OK,
    response_model=RewardResponse,
    responses=rewards_error_docs.claim_reward,
)
@request_logging
def claim_reward(
    reward_id: int,
    user: Annotated[CurrentUserEntity, Depends(get_current_user_entity)],
    use_case: Annotated[ClaimRewardUseCase, Depends(claim_reward_use_case)],
) -> RewardResponse:
    return use_case.execute(reward_id=reward_id, user_id=user.user_id)
