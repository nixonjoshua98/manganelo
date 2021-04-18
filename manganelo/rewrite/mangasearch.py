import ast
import string

from bs4 import BeautifulSoup

from manganelo.rewrite import utils, siterequests

from manganelo.rewrite.chapterlist import ChapterList

import functools as ft


class SearchResult:
	def __init__(self, soup):
		self._soup = soup

	@ft.cached_property
	def title(self): return self._soup.find(class_="item-img").get("title", None)

	@ft.cached_property
	def url(self): return self._soup.find(class_="item-img").get("href", None)

	@ft.cached_property
	def icon_url(self): return self._soup.find("img", class_="img-loading").get("src", None)

	@ft.cached_property
	def updated(self):
		s = self._soup.find("span", class_="text-nowrap item-time").text
		return utils.parse_date(s, "Updated : %b %d,%Y - %H:%M")

	@ft.cached_property
	def authors(self):
		return [e.strip() for e in self._soup.find("span", class_="text-nowrap item-author").text.split(",")]

	@ft.cached_property
	def views(self):
		s = self._soup.find_all("span", class_="text-nowrap item-time")[-1].text
		return ast.literal_eval(s.replace("View : ", "").replace(",", ""))

	@ft.cached_property
	def rating(self): return ast.literal_eval(self._soup.find("em", class_="item-rate").text)

	@ft.lru_cache()
	def chapter_list(self): return ChapterList(self.url).get()


class MangaSearch:
	def __init__(self, title: str):
		self._raw_title = title

	def get(self):
		r = self._send_request()

		return self._extract_response(r)

	def _send_request(self):
		return siterequests.search(self._validate_title(self._raw_title))

	def _extract_response(self, resp) -> list:
		soup = BeautifulSoup(resp.content, "html.parser")

		return [SearchResult(ele) for ele in soup.find_all(class_="search-story-item")]

	@staticmethod
	def _validate_title(title: str) -> str:
		allowed_characters: str = string.ascii_letters + string.digits + "_"

		return "".join([char.lower() for char in title.replace(" ", "_") if char in allowed_characters])
