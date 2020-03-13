import dataclasses
import typing
import ast

from manganelo.api import APIBase

@dataclasses.dataclass
class MangaChapter:
	url: str
	chapter_num: float


class MangaInfo(APIBase):
	url: str
	views: int
	title: str
	status: str
	last_updated: str
	genres: typing.List[str]
	authors: typing.List[str]
	alt_titles: typing.List[str]
	chapters: typing.List[MangaChapter]

	def __init__(self, url: str):
		super().__init__()

		self._url = url

		self.values = {}

		self._page_soup = self._get_soup()

		self._get_results()

	def __str__(self):
		return self._url

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		""" Context manager exit point """

	def _get_results(self):
		info_panel = self._page_soup.find(class_="panel-story-info")

		if info_panel is None:
			raise Exception(f"Invalid URL '{self._url}'")

		right_extend 		= info_panel.find(class_="story-info-right-extent")
		story_info_right 	= info_panel.find(class_="story-info-right")
		table_section 		= story_info_right.find(class_="variations-tableInfo")

		table_values 						= table_section.find_all(class_="table-value")
		last_updated_ele, views_ele, *_ 	= right_extend.find_all("span", class_="stre-value")

		chapters = self._get_chapters()

		self.values = {
			"title": story_info_right.find("h1").text,
			"authors": [author.strip() for author in table_values[1].text.split("-")],
			"genres": [genre.strip() for genre in table_values[3].text.split("-")],
			"alt_titles": table_values[0].text,
			"status": table_values[2].text,
			"url": self._url,
			"views": int(views_ele.text.replace(",", "")),
			"last_updated": last_updated_ele.text,
			"chapters": chapters,
			"num_chapters": len(chapters)
		}

		for k, v in self.values.items():
			setattr(self, k, v)

	def _get_chapters(self):
		panels = self._page_soup.find(class_="panel-story-chapter-list")

		ls = []

		for i, ele in enumerate(reversed(panels.find_all(class_="a-h"))):
			url = ele.find("a")["href"]

			chapter_num = ast.literal_eval(url.split("chapter_")[-1])

			chapter = MangaChapter(url=url, chapter_num=chapter_num)

			ls.append(chapter)

		return ls