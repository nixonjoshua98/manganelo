
from manganelo.api import MangaSearch
from manganelo.api import MangaInfo

if __name__ == "__main__":
	info = MangaInfo("https://manganelo.com/manga/zp922428")

	for k, v in info.values.items():
		print(f"{k}: {v}")

