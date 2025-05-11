from .base import BaseHTMLParser


class RFTodayParser(BaseHTMLParser):
    def __init__(self) -> None:
        super().__init__(
            url="https://finance.rftoday.ru/",
            tag="span",
            css_class="title",
        )
