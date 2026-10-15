from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.scheduler_service import scheduler_service
from app.services.system_monitor import system_monitor

router = APIRouter(prefix="/api/v1")


class SchedulerStartRequest(BaseModel):
    symbol: str = Field(default="AAPL", min_length=1, max_length=16)
    interval_seconds: int = Field(default=60, ge=10, le=86400)


@router.get("/system/status")
def system_status() -> dict[str, object]:
    return system_monitor.snapshot()


@router.get("/system/overview")
def system_overview() -> dict[str, object]:
    return system_monitor.snapshot()


@router.get("/system/metrics")
def system_metrics() -> dict[str, object]:
    snapshot = system_monitor.snapshot()
    return {
        "uptime_seconds": snapshot["uptime_seconds"],
        "scheduler": snapshot["scheduler"],
        "database_configured": snapshot["database_configured"],
        "alpaca_configured": snapshot["alpaca_configured"],
    }


@router.get("/system/scheduler/status")
def scheduler_status() -> dict[str, object]:
    return scheduler_service.status()


@router.post("/system/scheduler/start")
def start_scheduler(payload: SchedulerStartRequest) -> dict[str, object]:
    return scheduler_service.start(payload.symbol, payload.interval_seconds)


@router.post("/system/scheduler/stop")
def stop_scheduler() -> dict[str, object]:
    return scheduler_service.stop()
