from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.approval import router as approval_router
from app.api.routes.automation import router as automation_router
from app.api.routes.backtest import router as backtest_router
from app.api.routes.experiments import router as experiments_router
from app.api.routes.health import router as health_router
from app.api.routes.market import router as market_router
from app.api.routes.orders import router as orders_router
from app.api.routes.paper_trading import router as paper_trading_router
from app.api.routes.portfolio import router as portfolio_router
from app.api.routes.risk import router as risk_router
from app.api.routes.strategies import router as strategies_router
from app.api.routes.strategy_registry import router as strategy_registry_router
from app.api.routes.system import router as system_router
from app.api.routes.trade_history import router as trade_history_router
from app.api.routes.validation import router as validation_router
from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.db.init_db import init_db

settings = get_settings()
configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="EvoTrade AI",
    version="0.2.0",
    description="Self-improving multi-agent AI trading system for paper trading.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(market_router)
app.include_router(strategies_router)
app.include_router(risk_router)
app.include_router(orders_router)
app.include_router(backtest_router)
app.include_router(validation_router)
app.include_router(approval_router)
app.include_router(strategy_registry_router)
app.include_router(trade_history_router)
app.include_router(experiments_router)
app.include_router(paper_trading_router)
app.include_router(automation_router)
app.include_router(portfolio_router)
app.include_router(system_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "EvoTrade AI is running"}
