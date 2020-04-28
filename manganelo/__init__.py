
from manganelo.api import (MangaInfo, SearchManga, DownloadChapter)

__ALL__ = (
	"MangaInfo",
	"SearchManga",
	"DownloadChapter"
)

if __name__ == "__main__":
	from manganelo import (MangaInfo, SearchManga, DownloadChapter)

	# Perform a search for a Manga
	search = SearchManga("Mythical Realm", threaded=True)

	print("URL:", search.url)

	# Turn the generator into a list
	results = list(search.results())

	print("Number of search results:", len(results))

	# The top result from the search results
	best_result = results[0]

	# The page which showcases the Manga
	manga_info = MangaInfo(best_result.url, threaded=True)

	manga_page = manga_info.results()

	for attr in manga_page.__dir__():
		if attr.startswith("__"):
			continue

		print(f"{attr:30s}: {getattr(manga_page, attr)}")

	# Iterate through all the chapters
	for chapter in manga_page.chapters:
		file = f"./Naruto {chapter.chapter_num}.pdf"

		# Download the chapter
		#dl = DownloadChapter(chapter.url, file)

		#print(f"Downloaded: {dl.ok}")