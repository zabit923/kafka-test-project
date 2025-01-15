from fastapi import APIRouter

from .aplications.routers import router as aplication_router


router = APIRouter(prefix="/api/v1")
router.include_router(aplication_router, tags=["aplications"])
