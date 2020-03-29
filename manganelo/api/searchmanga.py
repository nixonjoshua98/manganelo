import string
import requests

from dataclasses import dataclass
from bs4 import BeautifulSoup

from manganelo.errors import (TagNotFound, RequestFailed)


@dataclass
class MangaSearchResult:
	title: str
	url: str


class SearchManga:
	def __init__(self, title: str) -> None:
		self.results = []
		self.url = "http://manganelo.com/search/" + self._format_title(title)

	def start(self):
		response = self._send_request(self.url)

		if response is None:
			raise RequestFailed(f"Request failed")

		soup = BeautifulSoup(response.content, "html.parser")
		panels = soup.find(class_="panel-search-story")

		if panels is None:
			raise TagNotFound(f"Tag 'panel-search-story' not found in response HTML")

		stories = panels.find_all(class_="search-story-item")

		for i, ele in enumerate(stories):
			item = ele.find(class_="item-img")

			if item is None:
				raise TagNotFound(f"Tag 'item-img' not found in response HTML")

			title, link = item["title"], item["href"]

			manga_result = MangaSearchResult(title=title, url=link)

			self.results.append(manga_result)

	@staticmethod
	def _send_request(url):
		default_headers = requests.utils.default_headers()

		r = requests.get(url, stream=True, timeout=5, headers=default_headers)

		r.raise_for_status()

		if r.status_code == requests.codes.ok:
			return r

	@staticmethod
	def _format_title(title: str) -> str:
		allowed_characters: str = string.ascii_letters + string.digits + "_"

		return "".join([char.lower() for char in title.replace(" ", "_") if char in allowed_characters])

	def __enter__(self):
		self.start()

		return self

	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		pass

	def __len__(self) -> int:
		return len(self.results)

	def __getitem__(self, item):
		return self.results[item]

	def __contains__(self, item):
		return item in self.results

	def __iter__(self):
		return iter(self.results)
