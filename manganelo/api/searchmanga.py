import string

from dataclasses import dataclass
from bs4 import BeautifulSoup

from manganelo import utils

from manganelo.api.api_base import APIBase


@dataclass(frozen=True)
class MangaSearchResult:
	title: str
	url: str


class SearchManga(APIBase):
	def __init__(self, query: str) -> None:
		"""
		:param query: Manga string to search for, we strip the 'illegal' characters ourselves.
		"""

		self.query: str = query
		self.results: list = []

	def __str__(self):
		""" Return the query string which was passed in at construction. """
		return self.query

	def __enter__(self):
		""" Context manager entry point. Call .start() before we return the instance. """
		self.start()

		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		""" Context manager exit point """

	def __len__(self) -> int:
		""" Return the length of the internal results list """
		return len(self.results)

	def __getitem__(self, item):
		""" Index the internal list """
		return self.results[item]

	def __contains__(self, item):
		""" Check if an item exists in the results """
		return item in self.results

	def __iter__(self):
		""" Used in loops. Simply return results.__iter__ """
		return iter(self.results)

	def start(self):
		""" This is where the magic happens. Sends the request and extracts the information we want. """

		# Generate the URL, which includes removing 'illegal' characters
		url = self._generate_url(self.query)

		# Send the request. Can also raise an exception is the request fails.
		response = self._send_request(url)

		# Entire page soup
		soup = BeautifulSoup(response.content, "html.parser")

		# List of the search results
		results = soup.find_all(class_="search-story-item")

		# Iterate over the results soup and extract the information we want
		for i, ele in enumerate(results):
			manga = utils.find_or_raise(ele, class_="item-img")

			title = manga.get("title", None)  # Manga title
			link = manga.get("href", None)  # Link to the manga 'homepage'

			r = MangaSearchResult(title=title, url=link)

			self.results.append(r)

	def _generate_url(self, query: str) -> str:
		"""
		Generate the URL we send the request to, we remove all 'illegal' characters here from the query string.

		:param str query: THe base query string which we are searching for
		:return str: Return the formatted URL
		"""
		allowed_characters: str = string.ascii_letters + string.digits + "_"

		query = "".join([char.lower() for char in query.replace(" ", "_") if char in allowed_characters])

		return self._SEARCH_URL + query
