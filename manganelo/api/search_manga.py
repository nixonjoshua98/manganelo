import string

from dataclasses import dataclass

from manganelo.common import constants
from manganelo.api.api_base import APIBase
from manganelo.exceptions import ObjectExpiredException


@dataclass
class MangaSearchResult:
	title: str
	url: str


class SearchManga(APIBase):
	def __init__(self, title: str, start: bool = False):
		"""
		:param title: Title of the Manga which is being searched.
		:param start: Choose to start the search straight away
		"""

		self.__title = title

		self._results = []

		self.__create_url()

		if start:
			self.start()

	def start(self):
		"""
		The 'main' method of the class which gets the soup and extracts the information.

		:raises ObjectExpiredException: Raises an exception which this object is re-used.
		"""

		if self._is_expired:
			raise ObjectExpiredException(f"{__name__} should not be reused.")

		self._is_expired = True

		soup = self._get_soup()

		# This is most likely caused because the website HTML has changed.
		if soup is None:
			return None

		self.__scrape(soup)

	def __create_url(self) -> None:
		self.__title = self.__title.lower()
		self.__title = self.__title.replace(" ", "_")

		alphanumeric = string.ascii_lowercase + string.digits

		# Remove punctuation etc.
		for i in self.__title:
			if i in {"_"}:
				continue

			if i not in alphanumeric:
				self.__title = self.__title.replace(i, "")

		# Add the newly formatted title to the URL
		self._url = constants.MANGANELO_SEARCH_URL + self.__title

	def __scrape(self, soup):
		panels = soup.find(class_="panel-search-story")
		stories = panels.find_all(class_="search-story-item")

		for i, ele in enumerate(stories):
			manga = ele.find(class_="item-img")

			row = MangaSearchResult(title=manga["title"], url=manga["href"])

			self._results.append(row)

