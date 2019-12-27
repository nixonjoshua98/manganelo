
from manganelo.api.manga_chapters import MangaChapters
from manganelo.tests.test_decorators import test_decorator
from manganelo.exceptions import ObjectExpiredException

url = "https://manganelo.com/manga/zl919985"


@test_decorator
def test_get_chapters():
	obj = MangaChapters(url, start=True)

	if len(obj.results) > 0:
		print("OK")


@test_decorator
def test_object_expiration():
	obj = MangaChapters(url, start=True)

	try:
		obj.start()

	except ObjectExpiredException:
		print("OK")


@test_decorator
def test_results_length():
	r1 = MangaChapters(url, start=True).results
	r2 = MangaChapters(url, start=True).results
	r3 = MangaChapters(url, start=True).results

	if len(r1) == len(r2) == len(r3):
		print("OK")


def run_all_tests():
	test_get_chapters()
	test_object_expiration()
	test_results_length()
