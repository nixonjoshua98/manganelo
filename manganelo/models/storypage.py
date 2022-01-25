import ast
import datetime as dt
from deprecated import deprecated

from .. import siterequests
from ..common import utils
from .chapter import Chapter
from ..common.types import NumberType


class StoryPage:
    __slots__ = ("url", "title", "icon_url", "description", "genres", "views", "authors", "updated", "chapters")

    def __init__(self, url, soup):
        self.url: str = url
        self.title: str = soup.find(class_="story-info-right").find("h1").text.strip()
        self.icon_url: str = soup.find("div", class_="story-info-left").find("img", class_="img-loading").get("src")
        self.description: str = utils.unescape_html(soup.find("div", class_="panel-story-info-description").text)
        self.genres: list[str] = self._parse_genres(soup)
        self.views: NumberType = self._parse_views(soup)
        self.authors: list[str] = self._parse_authors(soup)
        self.updated: dt.datetime = self._parse_updated(soup)
        self.chapters: list[Chapter] = self._parse_chapters(soup)

    @deprecated(reason="Use the chapters attribute instead for this class")
    def chapter_list(self):
        return self.chapters

    def download_icon(self, *, path: str):
        if img := siterequests.get_image(self.icon_url):
            return utils.save_image(img, path)

    @staticmethod
    def _parse_authors(soup):
        values = soup.find("table", class_="variations-tableInfo").find_all("td", class_="table-value")
        author = values[1]

        return [e.strip() for e in author.text.split(",")]

    @staticmethod
    def _parse_genres(soup):
        values = soup.find("table", class_="variations-tableInfo").find_all("td", class_="table-value")
        genres = values[3].find_all("a", class_="a-h")

        return [e.text.strip() for e in genres]

    @staticmethod
    def _parse_updated(soup) -> dt.datetime:
        values = soup.find("div", class_="story-info-right-extent").find_all("span", class_="stre-value")

        return utils.parse_date(values[0].text.strip(), "%b %d,%Y - %H:%M %p")

    @staticmethod
    def _parse_views(soup) -> NumberType:
        values = soup.find("div", class_="story-info-right-extent").find_all("span", class_="stre-value")

        s = values[1].text.strip()

        return ast.literal_eval(s.replace(",", ""))

    @staticmethod
    def _parse_chapters(soup) -> list[Chapter]:
        panels = soup.find(class_="panel-story-chapter-list")

        return [Chapter(ele) for ele in panels.find_all(class_="a-h")[::-1] if ele is not None]
