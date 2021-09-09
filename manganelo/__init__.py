
from .errors import *

from .chapterdownload import download_chapter

from .storypage import (
	get_story_page,

	StoryPage
)

from .storysearch import (
	get_search_results,

	Chapter,
	SearchResult
)


def get_chapter_list(url: str) -> list[Chapter]:
	return get_story_page(url).chapter_list()
