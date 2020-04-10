# Unofficial Manganelo API

#### Package to scrape the website Manganelo (and Mangakakalot)

###### Warning: API usages are still being worked on and may change over time

Installation
-

**Python 3.7 +**
```cmd
pip install manganelo
```

Usages
-

```python
from manganelo import (MangaInfo, SearchManga, DownloadChapter)

# Perform a search for a Manga
search = SearchManga("Naruto", threaded=False)

# Turn the generator into a list
results = list(search.results())

# Get the homepage of the first search result
info = MangaInfo(results[0].url)

# Iterate through all the chapters
for chapter in info["chapters"]:
    file = f"./Naruto {chapter.chapter_num}.pdf"

    # Download the chapter
    dl = DownloadChapter(chapter, file)

    print(f"Downloaded: {dl.ok}")
```

Contact Me
-

- nixonjoshua98-at-gmail-dot-com