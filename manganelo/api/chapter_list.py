import ast
import typing
import dataclasses

from manganelo.api import APIBase

@dataclasses.dataclass
class MangaChapter:
	url: str
	chapter_num: float


class ChapterList(APIBase):
	def __init__(self, url: str) -> None:
		"""
		:param url: The URL for the main page of the Manga
		"""
		super().__init__(url=url)

		self._chapters_soup = None

		self._validate_url()

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
		self.get()

		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		"""
		Exit point for the context managers, no need to do anything here

		:param exc_type:
		:param exc_val:
		:param exc_tb:
		:return:
		"""

	def get(self):
		"""
		Sends the page request and creates the soup ready for the results generator

		:return:
		:raises RequestFailedError: Raises if request and soupify'ing failed
		"""
		self._request_and_create_soup()

		panels = self._raw_soup.find(class_="panel-story-chapter-list")

		self._chapters_soup = panels.find_all(class_="a-h")

	def results(self) -> typing.Iterable[MangaChapter]:
		"""
		Extracts the relevant information from the soup and yields a result

		:return:
		"""
		def remove_redundant_zeroes(n: str):
			return int(n) if str(n).count(".") == 0 or str(n).endswith(".0") else float(n)

		for i, ele in enumerate(reversed(self._chapters_soup)):
			url = ele.find("a")["href"]

			chapter = ast.literal_eval(url.split("chapter_")[-1])

			yield MangaChapter(url=url, chapter_num=chapter)