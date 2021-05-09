from bs4 import BeautifulSoup

from manganelo.rewrite import utils, siterequests


class MangaPage:
	def __init__(self, soup):
		self._soup = soup

	def get(self):
		return self._extract_response()

	def _extract_response(self):
		panels = self._soup.find(class_="panel-story-chapter-list")

		return [Chapter(ele) for ele in panels.find_all(class_="a-h")[::-1] if ele is not None]


class MangaPageGetter:
	def __init__(self, url):
		self._url = url

	def get(self):
		return None
