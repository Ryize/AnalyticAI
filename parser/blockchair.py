from .base import BaseHTMLParser


class BlockchairParser(BaseHTMLParser):
    def __init__(self) -> None:
        super().__init__(
            url="https://blockchair.com/ru/news",
            tag="a",
            css_class="fs-lg fw-semibold link color-text-accent hover-underline",
        )
