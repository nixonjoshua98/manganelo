import string
import requests

from bs4 import BeautifulSoup
from typing import Union
from dataclasses import dataclass

from manganelo.common import constants


@dataclass
class MangaSearchResult:
	title: str
	url: str


class SearchManga:
	def __init__(self, title: str):
		self.__title = title
		self.__results = []

		self.__create_url()

	def search(self):
		soup = self.__get_soup()

		if soup is None:
			return None

		self.__scrape(soup)

	@property
	def results(self):
		return self.__results

	def __create_url(self) -> None:
		self.__title = self.__title.lower()
		self.__title = self.__title.replace(" ", "_")

		alphanumeric = string.ascii_lowercase + string.digits
		
		for i in self.__title:
			if i in {"_"}:
				continue

			if i not in alphanumeric:
				self.__title = self.__title.replace(i, "")

		self.__url = constants.MANGANELO_SEARCH_URL + self.__title

	def __get_soup(self) -> Union[BeautifulSoup, None]:
		headers = requests.utils.default_headers()

		try:
			r = requests.get(self.__url, stream=True, timeout=5, headers=headers)

			r.raise_for_status()

		except requests.exceptions.Timeout:
			pass

		except requests.exceptions.TooManyRedirects:
			pass

		except requests.exceptions.RequestException:
			pass

		else:
			return BeautifulSoup(r.content, "html.parser") if r.status_code == requests.codes.ok else None

	def __scrape(self, soup):
		panels = soup.find(class_="panel-search-story")
		stories = panels.find_all(class_="search-story-item")

		for i, ele in enumerate(stories):
			manga = ele.find(class_="item-img")

			row = MangaSearchResult(manga["title"], manga["href"])

			self.__results.append(row)

