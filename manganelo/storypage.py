import requests
from bs4 import BeautifulSoup

from .errors import RequestError
from .models import StoryPage


def get_story_page(url) -> StoryPage:
	r = requests.get(url)

	soup = BeautifulSoup(r.content, "html.parser")

	if "404" in soup.find("title").text:
		raise RequestError(f"Page '{url}' was not found")

	return StoryPage(url, soup)
