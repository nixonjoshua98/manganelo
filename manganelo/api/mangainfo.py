import dataclasses
import typing
import ast

from manganelo.api import APIBase

@dataclasses.dataclass
class MangaChapter:
	url: str
	chapter_num: float


class MangaInfo(dict, APIBase):
	def __init__(self, url: str):
		super().__init__()

		self._url = url

		self._page_soup = self._get_soup(url)

		self._parse_info()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		""" Context manager exit point """

	def _parse_info(self):
		# Elements
		info_panel 		= self._page_soup.find(class_="panel-story-info")
		info_right 		= info_panel.find(class_="story-info-right")
		right_extend 	= info_panel.find(class_="story-info-right-extent")

		try:
			last_updated_ele, views_ele, *_ = right_extend.find_all("span", class_="stre-value")
		except ValueError as e:
			raise ValueError(f"Some data could not be parsed")

		table = self._parse_table()

		# Data
		url			= self._url
		authors		= table["author"]
		status		= table["status"]
		genres 		= table["genres"]
		alt_titles 	= table.get("alternative", [])
		chapters 	= self._get_chapter_list()
		views 		= int(views_ele.text.replace(",", ""))
		updated_on	= last_updated_ele.text if last_updated_ele is not None else None
		title		= info_right.find("h1").text if info_right is not None else None

		self.update({
			"url": url, "authors": authors, "status": status, "genres": genres, "alt_titles": alt_titles,
			"chapters": chapters, "views": views, "updated_on": updated_on, "title": title
			})

	def _get_chapter_list(self):
		panels = self._page_soup.find(class_="panel-story-chapter-list")

		ls = []

		for i, ele in enumerate(reversed(panels.find_all(class_="a-h"))):
			if ele is not None:
				url = ele.find("a")["href"]
				chapter_num = ast.literal_eval(url.split("chapter_")[-1])
				chapter = MangaChapter(url=url, chapter_num=chapter_num)
				ls.append(chapter)

		return ls

	def _parse_table(self):
		table_section = self._page_soup.find(class_="variations-tableInfo")

		table_dict = {}

		if table_section is None:
			raise Exception(f"Table could not be found")

		for row in table_section.find_all("tr"):
			# Label amd the value elements
			lbl_ele, val_ele = row.find(class_="table-label"), row.find(class_="table-value")

			# e.g 'table-genres' to 'genres'
			key = lbl_ele.find("i").get("class")[0].split("-")[-1]

			val = None

			# Potential rows
			if key == "alternative":
				val = val_ele.text.strip().split(";")
			elif key == "author":
				val = val_ele.text.strip().split(",")
			elif key == "status":
				val = val_ele.text.strip()
			elif key == "genres":
				val = val_ele.text.strip().split("-")

			table_dict[key] = val

		return table_dict