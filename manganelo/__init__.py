
from manganelo.api import SearchManga
from manganelo.api import MangaInfo
from manganelo.api import DownloadChapter

from manganelo import api_

if __name__ == "__main__":
	search = api_.SearchMangaThread("Naruto")

	search.start()

	# do stuff here while we search in the background

	search.wait()

	for r in search:
		print(r)