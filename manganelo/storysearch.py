import ast
import string

import functools as ft

from bs4 import BeautifulSoup

from manganelo import siterequests
from manganelo.common import utils

from manganelo.storypage import get_story_page, Chapter


class SearchResult:
	def __init__(self, soup):
		self._soup = soup

	@ft.cached_property
	def title(self) -> str: return self._soup.find(class_="item-img").get("title")

	@ft.cached_property
	def url(self) -> str: return self._soup.find(class_="item-img").get("href")

	@ft.cached_property
	def icon_url(self) -> str: return self._soup.find("img", class_="img-loading").get("src")

	@ft.cached_property
	def updated(self):
		s = self._soup.find("span", class_="text-nowrap item-time").text

		return utils.parse_date(s, "Updated : %b %d,%Y - %H:%M")

	@ft.cached_property
	def authors(self) -> list[str]:
		return [e.strip() for e in self._soup.find("span", class_="text-nowrap item-author").text.split(",")]

	@ft.cached_property
	def views(self):
		s = self._soup.find_all("span", class_="text-nowrap item-time")[-1].text

		return ast.literal_eval(s.replace("View : ", "").replace(",", ""))

	@ft.cached_property
	def rating(self) -> float: return float(self._soup.find("em", class_="item-rate").text)

	@ft.cache
	def chapter_list(self) -> list[Chapter]:
		return get_story_page(self.url).chapter_list()

	def download_icon(self, path: str):
		if img := siterequests.get_image(self.icon_url):
			return utils.save_image(img, path)


def get_search_results(title: str) -> list[SearchResult]:
	allowed_characters: str = string.ascii_letters + string.digits + "_"

	title = "".join([char.lower() for char in title.strip().replace(" ", "_") if char in allowed_characters])

	r = siterequests.search(title)

	soup = BeautifulSoup(r.content, "html.parser")

	return [SearchResult(ele) for ele in soup.find_all(class_="search-story-item")]
