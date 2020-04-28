import string
import threading
import typing

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
		Constrctor for the object. We send the request here.

		:param str query: Query string which we will use as part of the URL which we will generate.
		:param bool threaded: Determines if we want to send the request on the main thread or spawn a new thread.
		"""

		self.url = None

		self._query = query
		self._response = None

		if threaded:
			# Create and start a new thread to send the request.

			self._thread = threading.Thread(target=self._start)

			self._thread.start()

		else:
			# Single-threaded - We call the start method on the main thread
			self._start()

	def _start(self) -> None:
		"""
		We generate the URL here and send the request.

		:raise: Exceptions from the requests module can be raised
		"""

		# Generate the URL, which includes removing 'illegal' characters
		self.url = self._generate_url(self._query)

		# Send the request. Can also raise an exception if the request fails.
		self._response = utils.send_request(self.url)

	def results(self) -> typing.Generator[MangaSearchResult, None, None]:
		"""
		Extract the results from the request we sent earlier.
		[Threaded] We join the thread, which means that we wait for the request to be finished.

		:return Generator: Return a generator of the results
		"""

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

		:param str query: The base query string which we are searching for
		:return str: Return the formatted URL
		"""
		allowed_characters: str = string.ascii_letters + string.digits + "_"

		query = "".join([char.lower() for char in query.replace(" ", "_") if char in allowed_characters])

		return "http://manganelo.com/search/" + query
