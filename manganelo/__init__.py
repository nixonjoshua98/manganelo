
from manganelo.api import MangaSearch
from manganelo.api import ChapterList
from manganelo.api import MangaInfo

if __name__ == "__main__":
	with MangaSearch("Naruto") as search_object:
		results = list(search_object.results())

		naruto = results[0]

	with ChapterList(naruto.url) as chap_list:
		chapters = list(chap_list.results())

	with MangaInfo(naruto.url) as info:
		naruto_info = info.result()

	print("Title:", naruto_info.title)
	print("Authors:", ",".join(naruto_info.authors))

	print("Total Chapters:", len(chapters))

	print("Latest Chapter URL:", chapters[-1].url)
