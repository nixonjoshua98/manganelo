import dataclasses
import typing
import ast

from manganelo.api import APIBase

@dataclasses.dataclass
class MangaChapter:
	url: str
	chapter_num: float


class MangaInfo(APIBase):
	url 		= None
	authors 	= None
	status 		= None
	genres 		= None
	alt_titles 	= None
	chapters 	= None
	views 		= None
	updated_on 	= None
	title 		= None

	def __init__(self, url: str):
		super().__init__()

		self.url = url

		self.values = {}

		self._page_soup = self._get_soup()

		self._parse()

	def __str__(self):
		return self.url

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		""" Context manager exit point """

	def _parse(self):
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
		self.url		= self.url
		self.authors	= table["author"]
		self.status		= table["status"]
		self.genres 	= table["genres"]
		self.alt_titles = table.get("alternative", [])
		self.chapters 	= self._get_chapter_list()
		self.views 		= int(views_ele.text.replace(",", ""))
		self.updated_on	= last_updated_ele.text if last_updated_ele is not None else None
		self.title		= info_right.find("h1").text if info_right is not None else None

		self.values = {
			"url": self.url, "authors": self.authors, "status": self.status, "genres": self.genres,
			"alt_titles": self.alt_titles, "chapters": self.chapters, "views": self.views,
			"updated_on": self.updated_on, "title": self.title
		}

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