from manganelo.common import utils

import datetime as dt


class HomeStoryTooltip:
    __slots__ = ("id", "name", "other_names", "authors", "genres", "description", "update_time")

    def __init__(self, data: dict):
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.other_names: list[str] = utils.split_at(data["nameother"], ";")
        self.authors: list[str] = utils.split_at(data["author"], ",")
        self.genres: list[str] = utils.split_at(data["genres"], ",")
        self.description: str = utils.unescape_html(data["description"])
        self.update_time: dt.datetime = utils.parse_date(data["updatetime"], "%b %d,%Y - %H:%M")

    def __str__(self):
        return f"{self.__class__.__name__}({', '.join([f'{ele}={getattr(self, ele)}' for ele in self.__slots__])})"

    def __repr__(self):
        return self.__str__()
