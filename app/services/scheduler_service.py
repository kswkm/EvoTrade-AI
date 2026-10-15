from __future__ import annotations

from dataclasses import dataclass, field

from apscheduler.schedulers.background import BackgroundScheduler

from app.services.automation import AutomationService


@dataclass
class SchedulerState:
    running: bool = False
    symbol: str = "AAPL"
    interval_seconds: int = 60
    job_id: str = "evotrade_cycle"
    jobs: list[str] = field(default_factory=list)


class SchedulerService:
    def __init__(self, automation_service: AutomationService | None = None) -> None:
        self.scheduler = BackgroundScheduler()
        self.automation = automation_service or AutomationService()
        self.state = SchedulerState()

    def _run_cycle(self) -> None:
        self.automation.run_cycle(self.state.symbol)

    def start(self, symbol: str = "AAPL", interval_seconds: int = 60) -> dict[str, object]:
        if self.scheduler.running:
            return {
                "status": "already_running",
                "symbol": self.state.symbol,
                "interval_seconds": self.state.interval_seconds,
                "job_id": self.state.job_id,
            }

        self.state.symbol = symbol.strip() or "AAPL"
        self.state.interval_seconds = max(10, int(interval_seconds))
        self.state.job_id = "evotrade_cycle"
        self.state.jobs = [self.state.job_id]

        self.scheduler.add_job(
            self._run_cycle,
            "interval",
            seconds=self.state.interval_seconds,
            id=self.state.job_id,
            replace_existing=True,
        )
        self.scheduler.start()
        self.state.running = True
        return {
            "status": "started",
            "symbol": self.state.symbol,
            "interval_seconds": self.state.interval_seconds,
            "job_id": self.state.job_id,
        }

    def stop(self) -> dict[str, object]:
        if not self.scheduler.running:
            return {"status": "stopped", "running": False, "job_id": self.state.job_id}

        self.scheduler.shutdown(wait=False)
        self.state.running = False
        self.state.jobs = []
        return {"status": "stopped", "running": False, "job_id": self.state.job_id}

    def status(self) -> dict[str, object]:
        return {
            "running": self.scheduler.running and self.state.running,
            "symbol": self.state.symbol,
            "interval_seconds": self.state.interval_seconds,
            "job_id": self.state.job_id,
        }


scheduler_service = SchedulerService()
