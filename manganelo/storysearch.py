import requests

from bs4 import BeautifulSoup

from manganelo.common import utils
from manganelo.common.constants import STORY_SEARCH_URL
from manganelo.errors import RequestError
from manganelo.models import SearchResult


def get_search_results(title: str) -> list[SearchResult]:
	r = requests.get(STORY_SEARCH_URL.format(title=utils.encode_querystring(title)))

	if r.status_code != 200:
		raise RequestError(f"Search request failed with status code {r.status_code}")

	soup = BeautifulSoup(r.content, "html.parser")

	return [SearchResult(ele) for ele in soup.find_all(class_="search-story-item")]
