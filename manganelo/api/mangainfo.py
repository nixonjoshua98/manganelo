import dataclasses
import typing
import threading
import ast

from datetime import datetime
from bs4 import BeautifulSoup

from manganelo import utils


@dataclasses.dataclass(frozen=True)
class MangaData:
    url: str
    title: str
    authors: list
    status: str
    genres: list
    alternative_titles: list
    chapters: list
    last_updated: datetime
    views: int
    icon: str
    description: str


@dataclasses.dataclass(frozen=True)
class MangaChapter:
    url: str
    title: str
    chapter_num: float


class MangaInfo:
    def __init__(self, url: str, *, threaded: bool = False):
        """
        Constrctor for the object. We send the request here.

        :param str url: The URL which we will send a request to
        :param bool threaded: Determines if we want to send the request on the main thread or spawn a new thread.
        """

        self.url = url

        self._soup = None

        if threaded:
            # Create and start a new thread to send the request.

            self._thread = threading.Thread(target=self._start)

            self._thread.start()

        else:
            # Single-threaded - We call the start method on the main thread
            self._start()

    def results(self) -> MangaData:
        """ Performs the soup extraction and returns an object """

        # If a thread object exists and it is still active, wait for it to finish.
        if hasattr(self, "_thread") and self._thread.is_alive():
            self._thread.join()

        table = self._parse_table()

        table.update(self._parse_extended_table())

        r = MangaData(
            url=self.url,
            title=self._get_title(),
            status=table.get("status", None),
            authors=table.get("author", []),
            genres=table.get("genres", []),
            alternative_titles=table.get("alternative", []),
            chapters=self._get_chapter_list(),
            last_updated=table.get("updated", None),
            views=table.get("views", 0),
            icon=self._get_icon(),
            description=self._get_description()
        )

        return r

    def _start(self) -> None:
        """ Send the request and create the soup object """

        response = utils.send_request(self.url)

        self._soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

    def _get_title(self) -> typing.Union[str, None]:
        """ Return the title present on the page """

        story_info_right = self._soup.find(class_="story-info-right")

        return getattr(story_info_right.find("h1"), "text", None)

    def _get_icon(self) -> str:
        info_panel = self._soup.find(class_="panel-story-info")
        info_left = info_panel.find(class_="story-info-left")
        image = info_left.find(class_="info-image")

        return image.find("img").get("src", None)

    def _get_description(self) -> str:
        info_panel = self._soup.find(class_="panel-story-info")
        description = info_panel.find(class_="panel-story-info-description")

        return description.text.replace("Description :", "").strip()

    def _get_chapter_list(self) -> typing.List[MangaChapter]:
        """
        Extract the chapter list from the website

        :return list: Return a list of chapters which each contain information about the chapter
        """

        panels = self._soup.find(class_="panel-story-chapter-list")

        ls = []

        for i, ele in enumerate(reversed(panels.find_all(class_="a-h"))):
            if ele is not None:
                url = ele.find("a")["href"]
                text = ele.find("a").text

                # Convert the string to the data type it needs. Eg 11.5 -> float | 10.0 -> int
                chapter_num = ast.literal_eval(url.split("chapter_")[-1])

                c = MangaChapter(url=url, chapter_num=chapter_num, title=text)

                ls.append(c)

        return ls

    def _parse_table(self) -> dict:
        """
        Parse the main table which contains the key information

        return dict: A dict of values taken from the page
        """

        table_section = self._soup.find(class_="variations-tableInfo")

        data = {}

        for row in table_section.find_all("tr"):
            label = row.find(class_="table-label")
            value = row.find(class_="table-value")

            # Eg. info-author -> author
            key = label.find("i").get("class")[0].split("-")[-1]
            val = None

            if key == "alternative":
                val = [ele.strip() for ele in value.text.split(";")]

            elif key == "author":
                val = [ele.text for ele in value.find_all("a")]

            elif key == "status":
                val = value.text.strip()

            elif key == "genres":
                val = [ele.text for ele in value.find_all("a")]

            data[key] = val

        return data

    def _parse_extended_table(self) -> dict:
        """
        Extract information from the extended table

        :return dict: Dict containing information taken from the extended table
        """

        right_extend = self._soup.find(class_="story-info-right-extent")

        rows = [ele.text for ele in right_extend.find_all("span", class_="stre-value") if ele.text.strip()]

        updated, views, *_ = rows

        # Remove AM and PM
        updated = updated[0:-3]

        updated = datetime.strptime(updated, "%b %d,%Y - %H:%M")
        views = int(views.replace(",", ""))

        return {"updated": updated, "views": views}
