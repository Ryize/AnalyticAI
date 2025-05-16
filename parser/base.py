import requests
from bs4 import BeautifulSoup
from typing import Optional, List
from logger import Logger
from abstract.parser import NewsParser


class BaseHTMLParser(NewsParser):
    def __init__(self, url: str, tag: str,
                 css_class: Optional[str] = None) -> None:
        self.url = url
        self.tag = tag
        self.css_class = css_class

    def parse(self) -> List[str]:
        response = requests.get(self.url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        elements = soup.find_all(self.tag,
                                 class_=self.css_class) if self.css_class else soup.find_all(
            self.tag)
        headlines: List[str] = [el.get_text(strip=True) for el in elements]
        res = []
        for i in headlines:
            if i[0].isdigit():
                res += i.split('назад')[1:]
        Logger().log(
            f"{self.__class__.__name__}: {len(res)} articles found")
        return res
