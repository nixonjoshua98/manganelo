
from manganelo.api import MangaSearch
from manganelo.api import MangaInfo

if __name__ == "__main__":
	info = MangaInfo("https://manganelo.com/manga/the_story_of_an_oneesan_who_wants_to_keep_a_high_school_boy")

	for k, v in info.values.items():
		print(f"{k}: {v}")

