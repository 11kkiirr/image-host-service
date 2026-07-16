from fastapi import APIRouter

from . import auth_route, profile_route, content_route, main_route, item_post_route, item_get_route

router = APIRouter()
router.include_router(auth_route.router)
router.include_router(profile_route.router)
router.include_router(content_route.router)
router.include_router(item_post_route.router)
router.include_router(item_get_route.router)
router.include_router(main_route.router)