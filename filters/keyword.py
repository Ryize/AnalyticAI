from typing import List
from abstract.parser import NewsFilter


class KeywordFilter(NewsFilter):
    def __init__(self, keywords: List[str]) -> None:
        super().__init__()
        self.keywords = keywords

    def _apply_filter(self, headlines: List[str]) -> List[str]:
        return [h for h in headlines if
                any(k.lower() in h.lower() for k in self.keywords)]
