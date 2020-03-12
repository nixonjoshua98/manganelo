import dataclasses
import typing

from manganelo.api import APIBase


@dataclasses.dataclass
class MangaInfoDC:
	title: str
	authors: typing.List[str]
	genres: typing.List[str]
	alt_titles: typing.List[str]
	status: str


class MangaInfo(APIBase):
	def __init__(self, url: str):
		super().__init__(url=url)

		self._info_panel = None

	def __str__(self) -> str:
		"""
		:return: Return the url which is passed at initialisation
		"""
		return self._url

	def __enter__(self):
		"""
		Entry point for context manager

		:return: Return the instance
		"""
		self.start()

		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		"""
		Exit point for the context managers, no need to do anything here

		:param exc_type:
		:param exc_val:
		:param exc_tb:
		:return:
		"""

	def start(self) -> None:
		self._request_and_create_soup()

		self._info_panel = self._raw_soup.find(class_="panel-story-info")

	def result(self) -> MangaInfoDC:
		story_info_right = self._info_panel.find(class_="story-info-right")
		table_section = story_info_right.find(class_="variations-tableInfo")
		table_values = table_section.find_all(class_="table-value")

		title = story_info_right.find("h1").text

		# Table values
		alt_titles = table_values[0].text
		status = table_values[2].text
		authors = [author.strip() for author in table_values[1].text.split("-")]
		genres = [genre.strip() for genre in table_values[3].text.split("-")]

		return MangaInfoDC(title=title, authors=authors, genres=genres, alt_titles=alt_titles, status=status)