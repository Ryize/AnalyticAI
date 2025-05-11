from typing import List, Optional
from abstract.parser import NewsFilter
from parser.factory import ParserFactory
from logger import Logger


class NewsAggregator:
    def __init__(self, sources: List[str],
                 filters: Optional[NewsFilter] = None) -> None:
        self.sources = sources
        self.filters = filters

    def get_news(self) -> List[str]:
        all_headlines: List[str] = []
        for source in self.sources:
            parser = ParserFactory.get_parser(source)
            if parser:
                all_headlines.extend(parser.parse())

        if self.filters:
            all_headlines = self.filters.handle(all_headlines)

        Logger().log(f"Total after filtering: {len(all_headlines)}")
        return all_headlines
