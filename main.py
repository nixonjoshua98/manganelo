
if __name__ == "__main__":
	from manganelo import SearchManga, MangaInfo, DownloadChapter

	search = SearchManga("Attack on Titan", threaded=False)
	results = search.results
	best_result = results[0]
	manga_info = MangaInfo(best_result.url, threaded=False)
	manga_page = manga_info.results

	file = f"./AoT {manga_page.chapters[0].title}.pdf"
	dl = DownloadChapter(manga_page.chapters[0].url, file)
	results = dl.results
	if results.saved_ok:
		print(results.path, results.percent_saved)

	exit()

	from manganelo import *

	search = SearchManga("Raid", threaded=False)

	results = search.results

	best_result = results[0]

	manga_info = MangaInfo(best_result.url, threaded=False)

	manga_page = manga_info.results

	for chapter in manga_page.chapters:

		file = f"./Raid {chapter.num}.pdf"

		dl = DownloadChapter(chapter.url, file)

		results = dl.results

		if results.saved_ok:
			print(results.path, results.percent_saved)
