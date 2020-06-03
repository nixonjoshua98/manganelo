
from manganelo.api import (MangaInfo, SearchManga, DownloadChapter, ChapterInfo)

__ALL__ = (
	"MangaInfo",
	"SearchManga",
	"DownloadChapter",
	"ChapterInfo"
)


if __name__ == "__main__":
	import os

	def main():
		search = SearchManga("Raid", threaded=False)

		results = list(search.results())

		best_result = results[0]

		manga_info = MangaInfo(best_result.url, threaded=False)

		manga_page = manga_info.results()

		for chapter in manga_page.chapters:
			file = f"./Raid {chapter.num}.pdf"

			dl = DownloadChapter(chapter.url, file)

			results = dl.results()

			if results.saved_ok:
				print(chapter.title, results.percent_saved, results.path)

				os.remove(results.path)

	main()
