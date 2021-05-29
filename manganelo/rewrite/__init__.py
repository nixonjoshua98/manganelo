

def search(*, title: str):
	from manganelo.rewrite.mangasearch import MangaSearch

	return MangaSearch(title).get()


def manga_page(*, url: str):
	from manganelo.rewrite.mangapage import MangaPageGetter

	return MangaPageGetter(url).get()


def chapter_list(*, url: str):
	return manga_page(url=url).chapter_list()


def download(*, url: str, path: str):
	from manganelo.rewrite.chapterdownloader import ChapterDownloader

	return ChapterDownloader(url).download(path)
