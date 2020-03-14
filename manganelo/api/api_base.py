import requests
import typing

from bs4 import BeautifulSoup


class APIBase:
	_SEARCH_URL = "http://manganelo.com/search/"

	def _get_soup(self) -> typing.Union[BeautifulSoup, None]:
		default_headers = requests.utils.default_headers()

		r = requests.get(self.url, stream=True, timeout=5, headers=default_headers)

		r.raise_for_status()

		return BeautifulSoup(r.content, "html.parser") if r.status_code == requests.codes.ok else None
