import ast

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
	def chapter(self): return ast.literal_eval(self.url.split("chapter_")[-1])

	@ft.cached_property
	def views(self):
		s = self._soup.find_all("span", class_="chapter-view text-nowrap")[-1].text
		return ast.literal_eval(s.replace(",", ""))

	@ft.cached_property
	def uploaded(self):
		s = self._soup.find("span", class_="chapter-time text-nowrap").get("title")
		return utils.parse_date(s, "%b %d,%Y %H:%M")

	def download(self, *, path): return ChapterDownloader(self.url).download(path)


class MangaPage:
	def __init__(self, soup):
		self._soup = soup

	@ft.lru_cache()
	def chapter_list(self):
		panels = self._soup.find(class_="panel-story-chapter-list")

		return [Chapter(ele) for ele in panels.find_all(class_="a-h")[::-1] if ele is not None]


class MangaPageGetter:
	def __init__(self, url):
		self._url = url

	def get(self):
		r = siterequests.get(self._url)

		soup = BeautifulSoup(r.content, "html.parser")

		return MangaPage(soup)
