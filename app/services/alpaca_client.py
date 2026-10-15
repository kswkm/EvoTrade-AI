from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from app.core.config import get_settings


class AlpacaClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.alpaca_api_key
        self.secret_key = settings.alpaca_secret_key
        self.base_url = settings.alpaca_base_url.rstrip("/")

    def _demo_bars(self, symbol: str, limit: int) -> list[dict[str, Any]]:
        now = datetime.now(timezone.utc)
        bars: list[dict[str, Any]] = []
        base = 100.0
        for i in range(limit):
            timestamp = (now - timedelta(days=limit - i)).strftime("%Y-%m-%dT%H:%M:%SZ")
            drift = (i % 5) * 0.75
            open_price = base + drift
            close_price = open_price + (0.8 if i % 2 == 0 else -0.7)
            high = max(open_price, close_price) + 1.2
            low = min(open_price, close_price) - 1.2
            bars.append(
                {
                    "symbol": symbol,
                    "timestamp": timestamp,
                    "open": round(open_price, 2),
                    "high": round(high, 2),
                    "low": round(low, 2),
                    "close": round(close_price, 2),
                    "volume": 1200 + i * 25,
                }
            )
        return bars

    def _headers(self) -> dict[str, str]:
        return {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key,
            "Content-Type": "application/json",
        }

    def get_account(self) -> dict[str, Any]:
        if not self.api_key or not self.secret_key:
            return {
                "account_blocked": False,
                "status": "paper",
                "cash": "100000.00",
                "equity": "100000.00",
                "trading_blocked": False,
            }

        try:
            response = httpx.get(
                f"{self.base_url}/v2/account",
                headers=self._headers(),
                timeout=15,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return {
                "account_blocked": False,
                "status": "paper",
                "cash": "100000.00",
                "equity": "100000.00",
                "trading_blocked": False,
            }

    def get_positions(self) -> list[dict[str, Any]]:
        if not self.api_key or not self.secret_key:
            return []

        try:
            response = httpx.get(
                f"{self.base_url}/v2/positions",
                headers=self._headers(),
                timeout=15,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return []

    def submit_order(self, symbol: str, side: str, qty: int, order_type: str = "market", time_in_force: str = "day") -> dict[str, Any]:
        if not self.api_key or not self.secret_key:
            return {
                "symbol": symbol,
                "side": side,
                "qty": qty,
                "status": "demo",
                "order_type": order_type,
                "time_in_force": time_in_force,
            }

        payload = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "type": order_type,
            "time_in_force": time_in_force,
            "order_class": "simple",
        }
        try:
            response = httpx.post(
                f"{self.base_url}/v2/orders",
                json=payload,
                headers=self._headers(),
                timeout=20,
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return {
                "symbol": symbol,
                "side": side,
                "qty": qty,
                "status": "simulated",
                "order_type": order_type,
                "time_in_force": time_in_force,
            }

    def get_market_data(self, symbol: str, limit: int = 30, timeframe: str = "1Day") -> list[dict[str, Any]]:
        if not self.api_key or not self.secret_key:
            return self._demo_bars(symbol, limit)

        try:
            from alpaca.data.historical import StockHistoricalDataClient
        except ImportError:
            return self._demo_bars(symbol, limit)

        try:
            client = StockHistoricalDataClient(self.api_key, self.secret_key, base_url=self.base_url)
            params = {"symbol_or_symbols": symbol, "limit": limit, "timeframe": timeframe}
            response = client.get_stock_bars(**params)
            if not response or symbol not in response:
                return self._demo_bars(symbol, limit)
            bars = response[symbol]
            return [
                {
                    "symbol": symbol,
                    "timestamp": bar.t.isoformat(),
                    "open": float(bar.o),
                    "high": float(bar.h),
                    "low": float(bar.l),
                    "close": float(bar.c),
                    "volume": int(bar.v),
                }
                for bar in bars
            ]
        except Exception:
            return self._demo_bars(symbol, limit)

    def get_market_data_via_rest(self, symbol: str, limit: int = 30, timeframe: str = "1Day") -> list[dict[str, Any]]:
        if not self.api_key or not self.secret_key:
            return self._demo_bars(symbol, limit)

        url = f"{self.base_url}/v2/stocks/{symbol}/bars"
        params = {"limit": limit, "timeframe": timeframe, "adjustment": "raw"}
        try:
            response = httpx.get(
                url,
                params=params,
                headers=self._headers(),
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            items = payload.get("bars", [])
            return [
                {
                    "symbol": symbol,
                    "timestamp": item.get("t", ""),
                    "open": float(item.get("o", 0.0)),
                    "high": float(item.get("h", 0.0)),
                    "low": float(item.get("l", 0.0)),
                    "close": float(item.get("c", 0.0)),
                    "volume": int(item.get("v", 0)),
                }
                for item in items
            ]
        except Exception:
            return self._demo_bars(symbol, limit)
