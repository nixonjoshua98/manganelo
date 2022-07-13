import ast

import functools as ft
import datetime as dt

from .chapter import Chapter
from manganelo import siterequests
from manganelo.common import utils


class SearchResult:
    __slots__ = ("title", "url", "icon_url", "authors", "rating", "views", "updated")

    def __init__(self, soup):
        self.title: str = soup.find(class_="item-img").get("title")
        self.url: str = soup.find(class_="item-img").get("href")
        self.icon_url: str = soup.find("img", class_="img-loading").get("src")
        self.authors: list[str] = self._parse_authors(soup)
        self.rating: float = float(soup.find("em", class_="item-rate").text)
        self.views: int = self._parse_views(soup)
        self.updated: dt.datetime = self._parse_updated(soup)

    @ft.cache
    def chapter_list(self) -> list[Chapter]:
        from manganelo.storypage import get_story_page  # Circular import

        return get_story_page(self.url).chapter_list()

    def download_icon(self, path: str):
        if img := siterequests.get_image(self.icon_url):
            return utils.save_image(img, path)

    @staticmethod
    def _parse_authors(soup) -> list[str]:
        authors = soup.find("span", class_="text-nowrap item-author")
        if authors:
          txt = authors.text
          return utils.split_at(txt, ",")
        else:
          return []

    @staticmethod
    def _parse_views(soup) -> int:
        s = soup.find_all("span", class_="text-nowrap item-time")[-1].text

        return ast.literal_eval(s.replace("View : ", "").replace(",", ""))

    @staticmethod
    def _parse_updated(soup) -> dt.datetime:
        s = soup.find("span", class_="text-nowrap item-time").text

        return utils.parse_date(s, "Updated : %b %d,%Y - %H:%M")
