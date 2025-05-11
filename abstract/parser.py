from abc import abstractmethod, ABC
from typing import List, Optional


class NewsParser(ABC):
    @abstractmethod
    def parse(self) -> List[str]:
        pass


class NewsFilter(ABC):
    def __init__(self):
        self._next: Optional[NewsFilter] = None

    def set_next(self, next_filter: 'NewsFilter') -> 'NewsFilter':
        self._next = next_filter
        return next_filter

    def handle(self, headlines: List[str]) -> List[str]:
        filtered = self._apply_filter(headlines)
        if self._next:
            return self._next.handle(filtered)
        return filtered

    @abstractmethod
    def _apply_filter(self, headlines: List[str]) -> List[str]:
        pass
