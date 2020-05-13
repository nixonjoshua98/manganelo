
from manganelo.api import (MangaInfo, SearchManga, DownloadChapter)

__ALL__ = (
	"MangaInfo",
	"SearchManga",
	"DownloadChapter"
)

if __name__ == "__main__":
	search = SearchManga("Naruto", threaded=True)

	results = list(search.results())

	best_result = results[0]

	manga_info = MangaInfo(best_result.url, threaded=True)

	manga_page = manga_info.results()

	for chapter in manga_page.chapters:
		file = f"./Naruto {chapter.num}.pdf"

		#dl = DownloadChapter(chapter.url, file)

		#print(f"Downloaded: {dl.ok}")
