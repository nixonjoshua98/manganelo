

def search(*, title: str):
	from manganelo.rewrite.mangasearch import SearchManga
	return SearchManga(title).get()


def chapters(*, url: str):
	from manganelo.rewrite.mangasearch import ChapterList

	return ChapterList(url).get()


def download(*, url: str, path: str):
	from manganelo.rewrite.chapterdownloader import ChapterDownloader

	return ChapterDownloader(url).download(path)
