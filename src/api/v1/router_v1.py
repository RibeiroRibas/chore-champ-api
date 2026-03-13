from fastapi import APIRouter

from src.api.v1.endpoints import auth_api, users_api, users_family_api, chores_api

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(auth_api.router, tags=["auth"])
router_v1.include_router(users_api.router, tags=["users"])
router_v1.include_router(users_family_api.router, tags=["family"])
router_v1.include_router(chores_api.router, tags=["chores"])
