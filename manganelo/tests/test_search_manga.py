from manganelo.api.search_manga import SearchManga


def test_search_manga():
	print(f"Test: {__name__}")

	search_object = SearchManga("Naruto")

	search_object.search()

	print("- Title: Naruto")
	print(f"- Num. Results: {len(search_object.results)}")


def run_all_tests():
	test_search_manga()
