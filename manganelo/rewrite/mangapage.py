import re
import ast
import typing

import functools as ft

from bs4 import BeautifulSoup

from manganelo.rewrite import utils, siterequests

from manganelo.rewrite.chapterdownloader import ChapterDownloader


class Chapter:
	def __init__(self, soup):
		self._soup = soup

	@ft.cached_property
	def title(self): return self._soup.find("a").text

	@ft.cached_property
	def url(self): return self._soup.find("a").get("href")

	@ft.cached_property
	def chapter(self):
		return ast.literal_eval(re.split("-|_", self.url.split("chapter")[-1])[-1])

	@ft.cached_property
	def views(self):
		s = self._soup.find_all("span", class_="chapter-view text-nowrap")[-1].text
		return ast.literal_eval(s.replace(",", ""))

	@ft.cached_property
	def uploaded(self):
		s = self._soup.find("span", class_="chapter-time text-nowrap").get("title")

		return utils.parse_date(s, "%b %d,%Y %H:%M")

	def download(self, *, path):
		return ChapterDownloader(self.url).download(path)


class MangaPage:
	def __init__(self, url, soup):
		self._soup = soup

		self.url = url

	@ft.cached_property
	def title(self): return self._soup.find(class_="story-info-right").find("h1").text.strip()

	@ft.cached_property
	def authors(self):
		values = self._soup.find("table", class_="variations-tableInfo").find_all("td", class_="table-value")
		author = values[1]

		return [e.strip() for e in author.text.split(",")]

	@ft.cached_property
	def genres(self):
		values = self._soup.find("table", class_="variations-tableInfo").find_all("td", class_="table-value")
		genres = values[3].find_all("a", class_="a-h")

		return [e.text.strip() for e in genres]

	@ft.cached_property
	def views(self):
		values = self._soup.find("div", class_="story-info-right-extent").find_all("span", class_="stre-value")

		s = values[1].text.strip()

		return ast.literal_eval(s.replace(",", ""))

	@ft.cached_property
	def icon_url(self): return self._soup.find("div", class_="story-info-left").find("img", class_="img-loading")["src"]

	@ft.cached_property
	def description(self): return self._soup.find("div", class_="panel-story-info-description").text.strip()

	@ft.lru_cache()
	def chapter_list(self) -> typing.List[Chapter]:
		panels = self._soup.find(class_="panel-story-chapter-list")

		return [Chapter(ele) for ele in panels.find_all(class_="a-h")[::-1] if ele is not None]

	def download_icon(self, *, path: str):
		if img := siterequests.dl_image(self.icon_url):
			return utils.save_image(img, path)


class MangaPageGetter:
	def __init__(self, url):
		self._url = url

	def get(self) -> MangaPage:
		r = siterequests.get(self._url)

		soup = BeautifulSoup(r.content, "html.parser")

		return MangaPage(self._url, soup)
