
if __name__ == "__main__":
	from manganelo import *

	search = SearchManga("Raid", threaded=False)

	results = search.results

	best_result = results[0]

	manga_info = MangaInfo(best_result.url, threaded=False)

	manga_page = manga_info.results

	for chapter in manga_page.chapters:
		continue

		file = f"./Raid {chapter.num}.pdf"

		dl = DownloadChapter(chapter.url, file)

		results = dl.results

		if results.saved_ok:
			print(results.path, results.percent_saved)
