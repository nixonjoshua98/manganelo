
from .errors import *
from .models import *

from .chapterdownload import download_chapter

from .storypage import (
	get_story_page,
	StoryPage
)

from .storysearch import (
	get_search_results,
	SearchResult
)

from .hometooltips import get_home_page


def get_chapter_list(url: str) -> list[Chapter]:
	return get_story_page(url).chapter_list()
