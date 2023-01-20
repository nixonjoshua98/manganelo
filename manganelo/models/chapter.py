import ast
import datetime as dt
import re

from pydantic import BaseModel

from ..chapterdownload import download_chapter
from ..common import utils
from typing import Union


class Chapter(BaseModel):
    title: str
    url: str
    chapter: Union[int, float]
    views: int
    uploaded: dt.datetime

    def download(self, path):
        return download_chapter(self.url, path)

    @staticmethod
    def from_soup(soup):
        obj = Chapter(
            title=_parse_title(soup),
            url=_parse_url(soup),
            chapter=-1,
            views=_parse_views(soup),
            uploaded=_parse_uploaded(soup)
        )

        obj.chapter = _parse_chapter(obj.url)

        return obj


def _parse_title(soup):
    return soup.find("a").text


def _parse_url(soup):
    return soup.find("a").get("href")


def _parse_chapter(url: str) -> Union[int, float]:
    return ast.literal_eval(re.split("[-_]", url.split("chapter")[-1])[-1])


def _parse_views(soup):
    s = soup.find_all("span", class_="chapter-view text-nowrap")[-1].text.replace(",", "")
    return utils.parse_views(s)


def _parse_uploaded(soup):
    s = soup.find("span", class_="chapter-time text-nowrap").get("title")
    return utils.parse_date(s, "%b %d,%Y %H:%M")
