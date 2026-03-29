from fastapi import APIRouter

from src.api.v1.endpoints import (
    auth_api,
    users_api,
    family_users_api,
    chores_api,
    day_of_week_api,
    rewards_api,
    legal_api,
)

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(auth_api.router, tags=["auth"])
router_v1.include_router(users_api.router, tags=["users"])
router_v1.include_router(family_users_api.router, tags=["family"])
router_v1.include_router(chores_api.router, tags=["chores"])
router_v1.include_router(day_of_week_api.router, tags=["days-of-week"])
router_v1.include_router(rewards_api.router, tags=["rewards"])
router_v1.include_router(legal_api.router, tags=["legal"])
