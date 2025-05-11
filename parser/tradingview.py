from .base import BaseHTMLParser


class TradingViewParser(BaseHTMLParser):
    def __init__(self) -> None:
        super().__init__(
            url="https://ru.tradingview.com/news/#news_markets",
            tag="article",
        )
