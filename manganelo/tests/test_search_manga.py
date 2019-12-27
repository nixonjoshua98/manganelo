
from manganelo.api.search_manga import SearchManga
from manganelo.tests.test_decorators import test_decorator
from manganelo.exceptions import ObjectExpiredException

title = "Naruto"


@test_decorator
def test_results_length():
	r1 = SearchManga(title, start=True).results
	r2 = SearchManga(title, start=True).results
	r3 = SearchManga(title, start=True).results

	if len(r1) == len(r2) == len(r3):
		print("OK")


@test_decorator
def test_object_expiration():
	obj = SearchManga(title, start=True)

	try:
		obj.start()

	except ObjectExpiredException:
		print("OK")


@test_decorator
def test_results_mutable():
	obj = SearchManga(title, start=True)

	results = obj.results

	results_length = len(results)

	results.pop(0)

	if len(obj.results) == results_length:
		print("OK")


def run_all_tests():
	test_results_length()
	test_object_expiration()
	test_results_mutable()
