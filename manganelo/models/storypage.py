import datetime as dt

from pydantic import BaseModel

from manganelo.common import utils
from manganelo.httpclient import _default_http_client
from manganelo.models.chapter import Chapter


class StoryPage(BaseModel):
    url: str
    title: str
    icon_url: str
    description: str
    genres: list[str]
    views: int
    authors: list[str]
    updated: dt.datetime
    chapter_list: list[Chapter]

    def download_icon(self, path: str):
        if img := _default_http_client.fetch_image(self.icon_url):
            return utils.save_image(img, path)

    @staticmethod
    def from_soup(url: str, soup) -> "StoryPage":
        return StoryPage(
            url=url,
            title=_parse_title(soup),
            icon_url=_parse_icon_url(soup),
            description=_parse_description(soup),
            genres=_parse_genres(soup),
            views=_parse_views(soup),
            authors=_parse_authors(soup),
            updated=_parse_updated(soup),
            chapter_list=_parse_chapters(soup)
        )


def _parse_title(soup):
    return soup.find(class_="story-info-right").find("h1").text.strip()


def _parse_icon_url(soup):
    return soup.find("div", class_="story-info-left").find("img", class_="img-loading").get("src")


def _parse_description(soup):
    return utils.unescape_html(soup.find("div", class_="panel-story-info-description").text)


def _parse_authors(soup):
    authors_row = soup.find("i", class_="info-author").findNext("td", class_="table-value")
    return [e.strip() for e in authors_row.text.split(" - ")]


def _parse_genres(soup):
    genres_row = soup.find("i", class_="info-genres").findNext("td", class_="table-value")
    genres = genres_row.find_all("a", class_="a-h")
    return [e.text.strip() for e in genres]


def _parse_updated(soup) -> dt.datetime:
    values = soup.find("div", class_="story-info-right-extent").find_all("span", class_="stre-value")
    return utils.parse_date(values[0].text.strip(), "%b %d,%Y - %H:%M %p")


def _parse_views(soup) -> int:
    values = soup.find("div", class_="story-info-right-extent").find_all("span", class_="stre-value")
    s = values[1].text.strip().replace(",", "")
    return utils.parse_views(s)


def _parse_chapters(soup) -> list[Chapter]:
    panels = soup.find(class_="panel-story-chapter-list")
    return [Chapter.from_soup(ele) for ele in panels.find_all(class_="a-h")[::-1] if ele is not None]
