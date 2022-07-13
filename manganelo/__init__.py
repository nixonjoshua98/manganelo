from .errors import RequestError, ManganeloError

from .models import Chapter, StoryPage, SearchResult, HomeStoryTooltip

from .chapterdownload import download_chapter
from .storypage import get_story_page
from .storysearch import get_search_results
from .hometooltips import get_home_page


def get_chapter_list(url: str) -> list[Chapter]:
	return get_story_page(url).chapter_list
