from abc import ABC, abstractmethod
from typing import Iterable, List, Dict, Any


class Analyzer(ABC):
    """Target‑интерфейс для модуля аналитики новостей."""

    @abstractmethod
    def analyze(self, headlines: Iterable[str], **kwargs) -> List[
        Dict[str, Any]]:
        """
        Принимает коллекцию строк (заголовков) и возвращает
        список словарей с произвольной структурой результата.
        """
        raise NotImplementedError
