
from manganelo.api import SearchManga
from manganelo.api import MangaInfo

if __name__ == "__main__":
	naruto = SearchManga("Naruto")[0]

	info = MangaInfo(naruto.url)

	for k, v in info.items():
		print(f"{k}: {v}")

