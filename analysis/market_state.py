from abc import ABC, abstractmethod


class MarketState(ABC):
    """Интерфейс состояния рынка."""

    @abstractmethod
    def message(self) -> str: ...


class BullishState(MarketState):
    def message(self) -> str:
        return "📈 Прогноз: акции, скорее всего, пойдут ВВЕРХ."


class BearishState(MarketState):
    def message(self) -> str:
        return "📉 Прогноз: ожидается снижение рынка."


class NeutralState(MarketState):
    def message(self) -> str:
        return "Рынок стабилен"
