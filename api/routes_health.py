from fastapi import APIRouter, Depends

from app.config import Settings
from app.dependencies import get_app_settings


router = APIRouter(tags=["health"])


@router.get("/health")
def health(settings: Settings = Depends(get_app_settings)) -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.service_name,
        "version": settings.version,
    }
