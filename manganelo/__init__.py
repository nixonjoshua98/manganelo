
from manganelo.api import (MangaInfo, SearchManga, DownloadChapter)

__ALL__ = (
	"MangaInfo",
	"SearchManga",
	"DownloadChapter"
)

if __name__ == "__main__":
	from manganelo import (MangaInfo, SearchManga, DownloadChapter)

	# Perform a search for a Manga
	search = SearchManga("Naruto", threaded=False)

	# Turn the generator into a list
	results = list(search.results())

	# Get the homepage of the first search result
	info = MangaInfo(results[0].url)

	# Iterate through all the chapters
	for chapter in info["chapters"]:
		file = f"./Naruto {chapter.chapter_num}.pdf"

		# Download the chapter
		dl = DownloadChapter(chapter.url, file)

		print(f"Downloaded: {dl.ok}")