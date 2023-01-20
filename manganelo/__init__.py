from .chapterdownload import download_chapter
from .errors import ManganeloError, RequestError
from .hometooltips import get_home_page
from .models import Chapter, HomeStoryTooltip, SearchResult, StoryPage
from .storypage import get_story_page
from .storysearch import get_search_results


def get_chapter_list(url: str) -> list[Chapter]:
	return get_story_page(url).chapter_list
