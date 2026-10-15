from app.schemas.trading import Signal
from app.strategies.base import BaseStrategy


class MovingAverageStrategy(BaseStrategy):
    name = "moving_average_crossover"

    def generate_signal(self, closes: list[float], symbol: str = "UNKNOWN") -> Signal:
        if len(closes) < 2:
            return Signal(symbol=symbol, direction="hold", confidence=0.0, rationale="Not enough data for MA signal")

        short_window = min(3, len(closes))
        long_window = min(5, len(closes))
        short_avg = sum(closes[-short_window:]) / short_window
        long_avg = sum(closes[-long_window:]) / long_window

        if short_avg > long_avg:
            return Signal(
                symbol=symbol,
                direction="buy",
                confidence=min(0.95, 0.5 + abs(short_avg - long_avg) / max(1.0, long_avg)),
                rationale=f"Short MA ({short_avg:.2f}) is above long MA ({long_avg:.2f})",
            )
        if short_avg < long_avg:
            return Signal(
                symbol=symbol,
                direction="sell",
                confidence=min(0.95, 0.5 + abs(long_avg - short_avg) / max(1.0, long_avg)),
                rationale=f"Short MA ({short_avg:.2f}) is below long MA ({long_avg:.2f})",
            )

        return Signal(
            symbol=symbol,
            direction="hold",
            confidence=0.5,
            rationale=f"Short MA ({short_avg:.2f}) is near long MA ({long_avg:.2f})",
        )
