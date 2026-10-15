from fastapi import APIRouter

from app.core.config import get_settings
from app.db.session import SessionLocal

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, object]:
    settings = get_settings()
    db_status = "unknown"
    try:
        with SessionLocal() as session:
            session.execute("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "unavailable"

    return {
        "status": "ok" if db_status in {"ok", "unknown"} else "degraded",
        "service": "evotrade-ai",
        "environment": settings.app_env,
        "database": db_status,
        "alpaca_configured": bool(settings.alpaca_api_key and settings.alpaca_secret_key),
    }
