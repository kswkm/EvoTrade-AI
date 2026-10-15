from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.walkforward import WalkforwardValidator

router = APIRouter(prefix="/api/v1")


class WalkforwardRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=16)
    closes: list[float] = Field(..., min_length=8)
    train_window: int = Field(default=5, ge=2)
    test_window: int = Field(default=3, ge=1)
    initial_cash: float = Field(default=100000.0, gt=0)


@router.post("/validation/walkforward")
def walkforward_validation(payload: WalkforwardRequest) -> dict[str, object]:
    validator = WalkforwardValidator(initial_cash=payload.initial_cash)
    result = validator.validate(
        payload.symbol,
        payload.closes,
        train_window=payload.train_window,
        test_window=payload.test_window,
    )
    return {
        "symbol": result.symbol,
        "average_test_return": round(result.average_test_return, 6),
        "pass_count": result.pass_count,
        "fold_count": len(result.folds),
        "folds": [
            {
                "train_start": fold.train_start,
                "train_end": fold.train_end,
                "test_start": fold.test_start,
                "test_end": fold.test_end,
                "train_return": round(fold.train_return, 6),
                "test_return": round(fold.test_return, 6),
                "pass_threshold": fold.pass_threshold,
            }
            for fold in result.folds
        ],
    }
