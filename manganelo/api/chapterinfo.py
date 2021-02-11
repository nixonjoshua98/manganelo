import dataclasses

import functools as ft

from typing import List

from bs4 import BeautifulSoup

from manganelo.api.apibase import APIBase


@dataclasses.dataclass
class ChapterInformation:
	title: str
	url: str
	image_urls: List[str]


class ChapterInfo(APIBase):
	def __init__(self, src_url: str, *, threaded: bool = False):

		self._src_url = src_url

		self._soup = None

		super(ChapterInfo, self).__init__(threaded=threaded)

	@classmethod
	def from_soup(cls, soup: BeautifulSoup):
		return ChapterInformation(
			title=cls._get_chapter_title(soup),
			url="N/A",
			image_urls=cls._get_image_urls(soup)
		)

	@ft.cached_property
	def results(self):
		self._join_thread()

		return ChapterInformation(
			title=self._get_chapter_title(self._soup),
			url=self._src_url,
			image_urls=self._get_image_urls(self._soup)
		)

	def _start(self) -> None:
		response = self.send_request(self._src_url)

		self._soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

	@classmethod
	def _get_image_urls(cls, soup) -> List[str]:
		"""
		Return all the image URLS inside the soup object.

		:return: We return a list of image URLS
		"""

		def valid(url: str):
			return url.endswith((".png", ".jpg"))

		image_soup = soup.find_all("img")

		images = [url for url in map(lambda ele: ele["src"], image_soup) if valid(url)]

		return images

	@classmethod
	def _get_chapter_title(cls, soup: BeautifulSoup) -> str:
		""" Return the title of the chapter. """

		title = soup.find(class_="panel-chapter-info-top")

		return title.find("h1").text if title else None
