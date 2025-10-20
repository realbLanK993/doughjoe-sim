from fastapi import APIRouter
from core.router import router as core_router
from room.router import router as room_router


router = APIRouter()

router.include_router(core_router, prefix="/", tags=["core"])

router.include_router(room_router, prefix="/", tags=["room"])
