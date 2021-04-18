

def search(*, title: str):
	from manganelo.rewrite.mangasearch import MangaSearch

	return MangaSearch(title).get()


def chapter_list(*, url: str):
	from manganelo.rewrite.chapterlist import ChapterList

	return ChapterList(url).get()


def download(*, url: str, path: str):
	from manganelo.rewrite.chapterdownloader import ChapterDownloader

	return ChapterDownloader(url).download(path)
