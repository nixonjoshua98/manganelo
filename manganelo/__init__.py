
from manganelo.api import MangaSearch
from manganelo.api import ChapterList
from manganelo.api import MangaInfo

if __name__ == "__main__":
	TITLE = "Nar"

	print("Search:", TITLE)

	results = MangaSearch(TITLE)

	print("Num. results:", len(results))

	first_result = results[0]

	print("URL:", first_result.url)

	print("Title:", first_result.title)

	chap_list = ChapterList(first_result.url)

	print("Num. Chapters:", len(chap_list))

	info = MangaInfo(first_result.url)

	print("Status:", info.status)
