from fastapi import APIRouter
from .core import router as core_router
from .room import router as room_router


router = APIRouter()

router.include_router(router=core_router.router, prefix="/core", tags=["core"])

router.include_router(room_router.router, prefix="/room", tags=["room"])
