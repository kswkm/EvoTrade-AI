from __future__ import annotations

import os
from datetime import datetime, timezone

from app.core.config import get_settings
from app.services.scheduler_service import scheduler_service


class SystemMonitor:
    def __init__(self) -> None:
        self.started_at = datetime.now(timezone.utc)

    def snapshot(self) -> dict[str, object]:
        settings = get_settings()
        uptime_seconds = int((datetime.now(timezone.utc) - self.started_at).total_seconds())
        build_sha = os.environ.get("GITHUB_SHA") or os.environ.get("BUILD_SHA") or "local"

        return {
            "status": "ready",
            "app_name": settings.app_name,
            "environment": settings.app_env,
            "version": "0.2.0",
            "build": build_sha,
            "mode": "paper_trading_only",
            "risk_engine": "enabled",
            "validation_required": True,
            "database_configured": bool(settings.database_url and settings.database_url.strip()),
            "alpaca_configured": bool(settings.alpaca_api_key and settings.alpaca_secret_key),
            "scheduler": scheduler_service.status(),
            "uptime_seconds": uptime_seconds,
            "features": {
                "market_data": True,
                "risk_checks": True,
                "backtesting": True,
                "walk_forward_validation": True,
                "strategy_registry": True,
                "paper_trading": True,
                "automation": True,
                "scheduler": True,
                "ci_pipeline": True,
            },
        }


system_monitor = SystemMonitor()
