import datetime as dt

from pydantic import BaseModel

from manganelo.common import utils
from manganelo.httpclient import _default_http_client

from .chapter import Chapter
from .storypage import StoryPage


class SearchResult(BaseModel):
    title: str
    url: str
    icon_url: str
    authors: list[str]
    rating: float
    views: int
    updated: dt.datetime

    @property
    def story_page(self) -> StoryPage:
        from manganelo.storypage import get_story_page  # Circular import

        return get_story_page(self.url)

    @property
    def chapter_list(self) -> list[Chapter]:
        return self.story_page.chapter_list

    def download_icon(self, path: str):
        if img := _default_http_client.fetch_image(self.icon_url):
            return utils.save_image(img, path)

    @staticmethod
    def from_soup(soup):
        return SearchResult(
            title=_parse_title(soup),
            url=_parse_url(soup),
            icon_url=_parse_icon_url(soup),
            authors=_parse_authors(soup),
            rating=_parse_rating(soup),
            views=_parse_views(soup),
            updated=_parse_updated(soup)
        )


def _parse_title(soup):
    return soup.find(class_="item-img").get("title")


def _parse_url(soup):
    return soup.find(class_="item-img").get("href")


def _parse_icon_url(soup):
    return soup.find("img", class_="img-loading").get("src")


def _parse_authors(soup):
    authors = soup.find("span", class_="text-nowrap item-author")
    return utils.split_at(authors.text, ",") if authors else []


def _parse_rating(soup):
    return float(soup.find("em", class_="item-rate").text)


def _parse_views(soup):
    s = soup.find_all("span", class_="text-nowrap item-time")[-1].text
    number_string = s.replace("View : ", "").replace(",", "")
    return utils.parse_views(number_string)


def _parse_updated(soup):
    s = soup.find("span", class_="text-nowrap item-time").text
    return utils.parse_date(s, "Updated : %b %d,%Y - %H:%M")