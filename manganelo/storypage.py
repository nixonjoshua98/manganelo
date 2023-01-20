from bs4 import BeautifulSoup

from manganelo.httpclient import _default_http_client

from .errors import RequestError
from .models import StoryPage


def get_story_page(url) -> StoryPage:
	r = _default_http_client.request("GET", url)

	soup = BeautifulSoup(r.content, "html.parser")

	if "404" in soup.find("title").text:
		raise RequestError(f"Page '{url}' was not found")

	return StoryPage.from_soup(url, soup)
