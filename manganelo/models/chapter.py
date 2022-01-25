import re
import ast
import datetime as dt

from ..common import utils
from ..common.types import NumberType
from ..chapterdownload import download_chapter


class Chapter:
    __slots__ = ("title", "url", "chapter", "views", "uploaded")

    def __init__(self, soup):
        self.title: str = soup.find("a").text
        self.url: str = soup.find("a").get("href")
        self.chapter: NumberType = self._parse_chapter(self.url)
        self.views: int = self._parse_views(soup)
        self.uploaded: dt.datetime = self._parse_uploaded(soup)

    def download(self, path):
        return download_chapter(self.url, path)

    @staticmethod
    def _parse_chapter(url: str) -> NumberType:
        return ast.literal_eval(re.split("[-_]", url.split("chapter")[-1])[-1])

    @staticmethod
    def _parse_views(soup):
        s = soup.find_all("span", class_="chapter-view text-nowrap")[-1].text
        return ast.literal_eval(s.replace(",", ""))

    @staticmethod
    def _parse_uploaded(soup):
        s = soup.find("span", class_="chapter-time text-nowrap").get("title")

        return utils.parse_date(s, "%b %d,%Y %H:%M")
