from bs4 import BeautifulSoup

from .errors import RequestError
from .models import StoryPage
from manganelo.httpclient import _default_http_client


def get_story_page(url) -> StoryPage:
	r = _default_http_client.request("GET", url)

	soup = BeautifulSoup(r.content, "html.parser")

	if "404" in soup.find("title").text:
		raise RequestError(f"Page '{url}' was not found")

	return StoryPage(url, soup)
