from abc import ABC, abstractmethod

from app.schemas.trading import Signal


class BaseStrategy(ABC):
    name: str = "base"

    @abstractmethod
    def generate_signal(self, closes: list[float], symbol: str = "UNKNOWN") -> Signal:
        raise NotImplementedError
