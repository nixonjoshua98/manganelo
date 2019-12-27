
from dataclasses import dataclass

from manganelo.api.api_base import APIBase
from manganelo.exceptions import ObjectExpiredException


@dataclass
class MangaChapter:
	url: str
	chapter_num: float


class MangaChapters(APIBase):
	def __init__(self, url: str, start: bool = False):
		"""
		:param url: URL of the Manga which the chapters are for.
		:param start: Choose to start straight away.
		"""

		self._url = url

		self._results = []

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

	def __scrape(self, soup):
		def remove_redundant_zeroes(n: str):
			return int(n) if str(n).count(".") == 0 or str(n).endswith(".0") else float(n)

		panels = soup.find(class_="panel-story-chapter-list")
		chapters = panels.find_all(class_="a-h")

		for i, ele in enumerate(reversed(chapters)):
			url = ele.find("a")["href"]
			chapter = remove_redundant_zeroes(url.split("chapter_")[-1])

			self._results.append(MangaChapter(url=url, chapter_num=chapter))
