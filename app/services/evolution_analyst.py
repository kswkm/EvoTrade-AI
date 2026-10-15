from __future__ import annotations

from app.schemas.trading import Signal


class EvolutionAnalyst:
    @staticmethod
    def classify_failure(reason: str) -> str:
        mapping = {
            "data": "DATA_ERROR",
            "signal": "SIGNAL_ERROR",
            "timing": "TIMING_ERROR",
            "size": "SIZING_ERROR",
            "cost": "COST_ERROR",
            "regime": "REGIME_SHIFT",
            "execution": "EXECUTION_ERROR",
            "thesis": "THESIS_INVALID",
        }
        lowered = reason.lower()
        for key, value in mapping.items():
            if key in lowered:
                return value
        return "THESIS_INVALID"

    @staticmethod
    def generate_experiment_hypothesis(failure_code: str, summary: str) -> dict:
        hypotheses = {
            "DATA_ERROR": "Validate source freshness and alternative data sources before trading.",
            "SIGNAL_ERROR": "Tighten signal criteria and compare against a baseline threshold.",
            "TIMING_ERROR": "Delay entry/exit by using time-based confirmation and lower volatility windows.",
            "SIZING_ERROR": "Reduce position sizing and attach bet sizing to volatility constraints.",
            "COST_ERROR": "Include slippage and spread assumptions in expected return calculation.",
            "REGIME_SHIFT": "Add regime filters to avoid trading when market conditions diverge.",
            "EXECUTION_ERROR": "Add retry guards and validate execution state before new orders are sent.",
            "THESIS_INVALID": "Re-test the thesis under identical conditions and use a stronger causal explanation.",
        }
        return {
            "failure_code": failure_code,
            "summary": summary,
            "hypothesis": hypotheses.get(failure_code, "Revisit the strategy assumptions with fresh evidence."),
        }

    @staticmethod
    def build_trade_review(signal: Signal, failure_reason: str) -> dict:
        failure_code = EvolutionAnalyst.classify_failure(failure_reason)
        return {
            "symbol": signal.symbol,
            "decision": signal.direction,
            "confidence": signal.confidence,
            "failure_code": failure_code,
            "failure_reason": failure_reason,
            "hypothesis": EvolutionAnalyst.generate_experiment_hypothesis(failure_code, failure_reason)["hypothesis"],
        }
