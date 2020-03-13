from __future__ import annotations  # Allows type hinting of own class (default in Python 4.0)

import typing

from manganelo.api import APIBase


class MangaInfo(APIBase):
	title: str
	authors: typing.List[str]
	genres: typing.List[str]
	alt_titles: typing.List[str]
	status: str

	def __init__(self, url: str):
		super().__init__()

		self._url = url

		self._values = {}

		self._page_soup = self._get_soup()

		self._get_results()

	def __str__(self) -> str:
		return self._url

	def __enter__(self) -> MangaInfo:
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		""" Context manager exit point """

	def _get_results(self) -> MangaInfoDC:
		info_panel = self._page_soup.find(class_="panel-story-info")

		story_info_right = info_panel.find(class_="story-info-right")
		table_section = story_info_right.find(class_="variations-tableInfo")

		table_values = table_section.find_all(class_="table-value")

		self._values = {
			"title": story_info_right.find("h1").text,
			"authors": [author.strip() for author in table_values[1].text.split("-")],
			"genres": [genre.strip() for genre in table_values[3].text.split("-")],
			"alt_titles": table_values[0].text,
			"status": table_values[2].text,
		}

		for k, v in self._values.items():
			setattr(self, k, v)