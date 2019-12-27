import requests

from typing import Union
from bs4 import BeautifulSoup


class APIBase:
	_url = None
	_is_expired = False
	_results = []

	def _get_soup(self) -> Union[BeautifulSoup, None]:
		"""
		Sends the server requests and soups the content.

		:returns: Returns either None or a soup object.
		"""

		headers = requests.utils.default_headers()

		try:
			r = requests.get(self._url, stream=True, timeout=5, headers=headers)

			r.raise_for_status()  # Raise for 404 etc.

		except requests.exceptions.Timeout:
			return None
		else:
			return BeautifulSoup(r.content, "html.parser") if r.status_code == requests.codes.ok else None

	@property
	def results(self):
		"""
		:returns: Returns a copy of the 'private' attribute, so that the user cannot
				edit the internal structure.
		"""

		return self._results[::]
