import requests

from bs4 import BeautifulSoup


class APIBase:
	def __init__(self, url: str = None):
		"""

		:param url:
		"""
		self._url = url
		self._raw_soup = None

	def get(self):
		raise NotImplementedError("APIBase.get -> NotImplemented")

	def _request_and_create_soup(self) -> bool:
		"""
		Send the request and turn the result into soup

		:return:
		"""
		default_headers = requests.utils.default_headers()

		# Send the request...
		r = requests.get(self._url, stream=True, timeout=5, headers=default_headers)

		# Set the soup value if the request went through OK
		if r.status_code == requests.codes.ok:
			self._raw_soup = BeautifulSoup(r.content, "html.parser")

			return self._raw_soup is not None  # True

		else:
			return False