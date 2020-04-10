
from manganelo.api import (MangaInfo, SearchManga, DownloadChapter)

from manganelo import extras

__ALL__ = (
	"extras",
	"MangaInfo",
	"SearchManga",
	"DownloadChapter"
)

if __name__ == "__main__":
	x = extras.SearchMangaThread("Naruto")

	x.start()

	print(x.results)