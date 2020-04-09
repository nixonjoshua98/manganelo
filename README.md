# Unofficial Manganelo API

#### Package to scrape the website Manganelo (and Mangakakalot)

nixonjoshua98 at gmail dot com

Installation
-

**Python 3.7.x**
```cmd
pip install manganelo
```

Usages
-

**Manga Search**

```python
from manganelo import SearchManga

search = SearchManga("Naruto")

search.start()

for result in search:
    print(result.title, result.url)
```

**Manga Info**

```python
from manganelo import MangaInfo

# ...

info = MangaInfo(search[0].url)

for k, v in info.items():
    print(f"{k}: {v}")
```

**Download Chapters**

```python
from manganelo import DownloadChapter

# ...

for chapter in info.get("chapters", []):
    file = f"./Naruto {chapter.chapter_num}.pdf"

    dl = DownloadChapter(chapter, file)

    print(f"Downloaded: {dl.ok}")
```

Extra API
-

An extra set of functionality can be found in **manganelo.extras** which are currently being developed and tested

```python
from manganelo import extras

search = extras.SearchMangaThread("Naruto")

search.start()  # Start the search thread

# do stuff here while we search in the background

search.wait()  # Wait for the search to finish if it hasn't already

for r in search:
    print(r)
```
