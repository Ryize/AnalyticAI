from analysis.market_state import MarketState
from analysis.market_state import (BullishState, BearishState,
                                   NeutralState)

class MarketContext:
    """
    Контекст, хранящий текущее состояние рынка и
    переключающийся в зависимости от итоговой тональности новостей.
    """

    def __init__(self):
        self._state: MarketState = NeutralState()

    def set_state(self, state: "MarketState"):
        self._state = state

    def forecast(self) -> str:
        return self._state.message()

    # бизнес-логика вычисления состояния
    def update_from_analysis(self, analyzed: list[dict]):
        if not analyzed:
            self._state = NeutralState()
            return

        pos = sum(1 for a in analyzed if a.get("sentiment") == "positive")
        neg = sum(1 for a in analyzed if a.get("sentiment") == "negative")

        if pos > neg:
            self._state = BullishState()
        elif neg > pos:
            self._state = BearishState()
        else:
            self._state = NeutralState()
