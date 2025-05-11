from typing import List
from abstract.parser import NewsFilter


class LengthFilter(NewsFilter):
    def __init__(self, min_length: int) -> None:
        super().__init__()
        self.min_length = min_length

    def _apply_filter(self, headlines: List[str]) -> List[str]:
        return [h for h in headlines if len(h) >= self.min_length]
