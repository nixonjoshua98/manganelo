import string
import threading

from typing import Generator
from bs4 import BeautifulSoup
from dataclasses import dataclass

from manganelo import utils


@dataclass(frozen=True)
class MangaSearchResult:
	title: str
	url: str


class SearchManga:
	def __init__(self, query: str, *, threaded: bool = False) -> None:
		"""
		:param query: Query string to search for, we strip the 'illegal' characters ourselves.
		"""
		self.query: str = query

		self._response = None

		if threaded:
			self._thread = threading.Thread(target=self._start)

			self._thread.start()
		else:
			self._start()

	def _start(self) -> None:
		""" Send the server request """

		# Generate the URL, which includes removing 'illegal' characters
		url = self._generate_url(self.query)

		# Send the request. Can also raise an exception is the request fails.
		self._response = utils.send_request(url)

	def results(self) -> Generator[MangaSearchResult, None, None]:
		""" Extract the information here """

		# If a thread object exists and it is still active, wait for it to finish.
		if hasattr(self, "_thread") and self._thread.is_alive():
			self._thread.join()

		# Entire page soup
		soup = BeautifulSoup(self._response.content, "html.parser")

		# List of the search results
		results = soup.find_all(class_="search-story-item")

		# Iterate over the results soup and extract the information we want
		for i, ele in enumerate(results):
			manga = utils.find_or_raise(ele, class_="item-img")

			title = manga.get("title", None)  # Manga title
			link = manga.get("href", None)  # Link to the manga 'homepage'

			yield MangaSearchResult(title=title, url=link)

	@staticmethod
	def _generate_url(query: str) -> str:
		"""
		Generate the URL we send the request to, we remove all 'illegal' characters here from the query string.

		:param str query: THe base query string which we are searching for
		:return str: Return the formatted URL
		"""
		allowed_characters: str = string.ascii_letters + string.digits + "_"

		query = "".join([char.lower() for char in query.replace(" ", "_") if char in allowed_characters])

		return "http://manganelo.com/search/" + query
