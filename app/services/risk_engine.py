from app.schemas.trading import AccountSnapshot, OrderCandidate, RiskDecision


class RiskEngine:
    def __init__(
        self,
        max_position_value: float = 100000.0,
        max_daily_loss_pct: float = 0.05,
        max_order_value_pct: float = 0.20,
    ) -> None:
        self.max_position_value = max_position_value
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_order_value_pct = max_order_value_pct

    def evaluate_order(self, candidate: OrderCandidate, account: AccountSnapshot) -> RiskDecision:
        reasons: list[str] = []

        if account.emergency_stop:
            reasons.append("emergency stop is active")

        if candidate.side == "hold":
            return RiskDecision(allowed=False, reasons=["order side is hold"], max_position_value=self.max_position_value)

        if candidate.order_value <= 0:
            reasons.append("order value must be greater than zero")

        if candidate.order_value > self.max_position_value:
            reasons.append("order exceeds maximum position value")

        position_value = account.current_positions.get(candidate.symbol, 0.0)
        projected_position_value = position_value + candidate.order_value
        if projected_position_value > self.max_position_value:
            reasons.append("projected position value exceeds allowed cap")

        if account.daily_loss_pct > self.max_daily_loss_pct:
            reasons.append("daily loss threshold exceeded")

        if candidate.order_value > (account.cash * self.max_order_value_pct):
            reasons.append("order value exceeds allowed percentage of cash")

        if candidate.side == "sell" and candidate.quantity <= 0:
            reasons.append("sell order quantity must be positive")

        projected_equity = account.equity + (candidate.order_value if candidate.side == "buy" else -candidate.order_value)
        return RiskDecision(
            allowed=not reasons,
            reasons=reasons,
            max_position_value=self.max_position_value,
            projected_post_trade_equity=projected_equity,
        )


def build_default_risk_engine() -> RiskEngine:
    from app.core.config import get_settings

    settings = get_settings()
    return RiskEngine(
        max_position_value=settings.risk_max_position_value,
        max_daily_loss_pct=settings.risk_max_daily_loss_pct,
        max_order_value_pct=settings.risk_max_order_value_pct,
    )
