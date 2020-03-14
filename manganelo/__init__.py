
from manganelo.api import SearchManga
from manganelo.api import MangaInfo
from manganelo.api import DownloadChapter

if __name__ == "__main__":
	naruto = SearchManga("Naruto")[0]

	info = MangaInfo(naruto.url)

	for k, v in info.items():
		print(f"{k}: {v}")

	download = DownloadChapter(info["chapters"][0].url, "./Naruto.pdf")

	print(f"Downloaded: {download.ok}")

