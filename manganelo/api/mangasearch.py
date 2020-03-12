import string
import typing
import dataclasses

from manganelo.common.constants import MANGANELO_SEARCH_URL

from manganelo.common import exceptions

from manganelo.api import APIBase


@dataclasses.dataclass
class MangaSearchResult:
	title: str
	url: str


class MangaSearch(APIBase):
	def __init__(self, title: str) -> None:
		"""
		:param title: The title of the manga which is to be searched for
		"""
		super().__init__()

		self._title = title
		self._results = []

		self._stories_soup = None

		self._format_title()
		self._create_and_validate_url()

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
		"""
		Sends the page request and creates the soup ready for the results generator

		:return:
		"""

		self._request_and_create_soup()

		panels = self._raw_soup.find(class_="panel-search-story")

		self._stories_soup = panels.find_all(class_="search-story-item")

	def results(self) -> typing.Iterable[MangaSearchResult]:
		"""
		Extracts the relevant information from the soup and yields a result

		:return: Returns a generator which contains the results from the soup
		"""
		for i, ele in enumerate(self._stories_soup):
			item = ele.find(class_="item-img")

			title = item["title"]
			link = item["href"]

			manga_result = MangaSearchResult(title=title, url=link)

			yield manga_result

	def _format_title(self) -> None:
		"""
		Format the title provided at initialisation to avoid errors when searching

		e.g. Punctuation will be ignored by Manganelo so we shouldn't send it as results may differ

		:return:
		"""
		title = self._title.lower()
		title = title.replace(" ", "_")

		# Acceptable characters
		alphanumeric = string.ascii_lowercase + string.digits

		# Remove all invalid characters from the title
		# This for sure can be improved
		for i, char in enumerate(title):
			if char == "_":
				continue

			if char not in alphanumeric:
				title = title.replace(char, "")

		self._title = title

	def _create_and_validate_url(self) -> None:
		"""
		Create the url and do any last minute validation needed

		:return:
		"""
		if len(self._title) < 3:
			raise exceptions.SearchTitleLengthError(f"Manga title '{self._title}' must have a length greater than 3")

		self._url = MANGANELO_SEARCH_URL + self._title
