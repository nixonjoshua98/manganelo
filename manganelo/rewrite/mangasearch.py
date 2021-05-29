import ast
import string
import typing

import functools as ft

from bs4 import BeautifulSoup

from . import utils, siterequests

from manganelo.rewrite.mangapage import MangaPageGetter, Chapter


class SearchResult:
	def __init__(self, soup):
		self._soup = soup

	@ft.cached_property
	def title(self): return self._soup.find(class_="item-img").get("title")

	@ft.cached_property
	def url(self): return self._soup.find(class_="item-img").get("href")

	@ft.cached_property
	def icon_url(self): return self._soup.find("img", class_="img-loading").get("src")

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
	def chapter_list(self) -> typing.List[Chapter]:
		return MangaPageGetter(self.url).get().chapter_list()

	def download_icon(self, *, path: str):
		if img := siterequests.dl_image(self.icon_url):
			return utils.save_image(img, path)


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
