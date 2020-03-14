import requests
import typing

from bs4 import BeautifulSoup


class APIBase:
	_SEARCH_URL = "http://manganelo.com/search/"

	@staticmethod
	def _get_soup(url: str) -> typing.Union[BeautifulSoup, None]:
		r = APIBase._send_request(url)

		if r.status_code == requests.codes.ok:
			return BeautifulSoup(r.content, "html.parser")

	@staticmethod
	def _send_request(url: str):
		default_headers = requests.utils.default_headers()

		r = requests.get(url, stream=True, timeout=5, headers=default_headers)

		r.raise_for_status()

		if r.status_code == requests.codes.ok:
			return r