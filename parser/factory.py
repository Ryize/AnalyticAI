from typing import Dict, Type, Optional
from abstract.parser import NewsParser
from .rftoday import RFTodayParser
from .blockchair import BlockchairParser
from .tradingview import TradingViewParser
from logger import Logger


class ParserFactory:
    _parsers: Dict[str, Type[NewsParser]] = {
        'rftoday': RFTodayParser,
        'blockchair': BlockchairParser,
        'tradingview': TradingViewParser,
    }

    @classmethod
    def get_parser(cls, source: str) -> Optional[NewsParser]:
        parser_cls = cls._parsers.get(source)
        if parser_cls:
            return parser_cls()
        Logger().log(f"Unknown parser source: {source}")
