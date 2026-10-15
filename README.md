# EvoTrade AI

EvoTrade AI is a self-improving multi-agent AI trading system designed for simulated U.S. stock trading. The project follows the development plan in the product requirements document and starts with a safe, testable foundation.

## Goals

- collect market data from Alpaca
- run deterministic risk checks before any order is accepted
- analyze trade outcomes and classify failures
- compare baseline and candidate strategies with evidence
- keep all strategy promotion behind validation gates

## Current scaffold

This repository now contains a near-production paper-trading implementation:

- FastAPI app with health, market, strategy, risk, order, paper-trading, automation, and system endpoints
- SQLAlchemy models for account, positions, orders, trades, experiments, and strategy versions
- risk engine that blocks dangerous or unverified orders
- market data validation and signal generation pipeline
- backtest, walk-forward validation, and strategy approval gate
- paper-trading execution flow with safe fallback behavior
- automation and scheduler support for periodic evaluation cycles
- monitoring endpoints for runtime status and operational readiness
- tests covering risk checks, strategy logic, market validation, backtesting, automation, and system health
- Docker Compose for PostgreSQL and Alembic support

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Copy environment settings:

```bash
copy .env.example .env
```

4. Start the app locally:

```bash
uvicorn app.main:app --reload
```

5. Run the app in production-like container mode:

```bash
docker compose up --build
```

6. Deploy with the production stack:

```bash
bash scripts/deploy.sh
```

7. Test the project:

```bash
python -m pytest -q
```

## Free deployment recommendation

The most budget-friendly option is Render's free tier:

- Web service: free tier for the FastAPI app
- Postgres database: free tier for the backing database
- No local server required for basic use
- Easy GitHub-connected deploys via Render dashboard or render.yaml

Example setup:

1. Push this repo to GitHub.
2. Create a Render account.
3. Import the repo and select this project.
4. Render will read `render.yaml` and provision the app + Postgres automatically.
5. Add `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` in Render's environment settings.

## API examples

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/system/status
curl -X POST http://localhost:8000/api/v1/market/signal \
  -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","close_prices":[100,101,102,103,104,105,106,107,108,109]}'
curl -X POST http://localhost:8000/api/v1/risk/validate-order \
  -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","side":"buy","quantity":10,"price":100.0,"cash":100000,"equity":100000,"current_positions":{}}'
```

## Safety principles

- No live trading by default.
- AI suggestions are never treated as direct execution authority.
- Trade execution must pass the risk engine.
- Experimental strategies are not promoted without validation.

## Tech stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alpaca API
- Pytest
