from __future__ import annotations  # Allows type hinting of own class (default in Python 4.0)

import ast
import typing
import dataclasses

from manganelo.api import APIBase

@dataclasses.dataclass
class MangaChapter:
	url: str
	chapter_num: float


class ChapterList(list, APIBase):
	def __init__(self, url: str) -> None:
		super().__init__()

		self._url = url

		self._page_soup = self._get_soup()

		self._get_results()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		""" Context manager exit point """

	def _get_results(self) -> typing.Iterable[MangaChapter]:
		panels = self._page_soup.find(class_="panel-story-chapter-list")

		chapters_soup = panels.find_all(class_="a-h")

		for i, ele in enumerate(reversed(chapters_soup)):
			url = ele.find("a")["href"]

			chapter_num = ast.literal_eval(url.split("chapter_")[-1])

			chapter = MangaChapter(url=url, chapter_num=chapter_num)

			self.append(chapter)