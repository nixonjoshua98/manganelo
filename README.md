# Unofficial Manganelo API

###### Package to scrape the Manganelo website. Pull requests are encouraged!

Installation
-
**Python 3.7 +**
```cmd
pip install manganelo
```

Examples
-

##### Manga searching
```python
from manganelo import SearchManga

"""
Threaded
    Request is made on a seperate thread and is joined when results() is called, 
    this means that you can do things while the request is being sent.

Not threaded (Single-threaded):
    Request is made on the same thread meaning execution will halt while it is sent
"""
search = SearchManga("Mythical Realm", threaded=True)

# .results() returns a generator - We create a list from the generator here
results = list(search.results())

# results = [MangaSearchResult(title=?, url=?), MangaSearchResult(title=?, url=?)]
```

##### Indiviual Manga Homepage
```python
...

from manganelo import MangaInfo

best_result = results[0]

manga_info = MangaInfo(best_result.url, threaded=True)

manga_page = manga_info.results()
```

##### Indiviual Manga Homepage Data (manga_page)

*Search Query: Mythical Realm*

Attribute | Value (Shortened)
--- | ---
url                | https://manganelo.com/manga/the_mythical_realm
title              | The Mythical Realm
authors            | ['Wu Zui', 'Liao Jia Le']
status             | Ongoing
genres             | ['Action', 'Adventure', 'Comedy', 'Fantasy', 'Manhua', 'Martial arts', 'Shounen']
alternative_titles | ['仙侠世界 (Chinese)', 'Xian Xia Shi Jie', 'Thế Giới Tiên Hiệp (Vietnamese - Tiếng Việt - TV)']
chapters           | [MangaChapter(url='https://manganelo.com/chapter/the_mythical_realm/chapter_0', title='Chapter 0 : Prologue', num=0)...]
last_updated       | 2020-04-28 23:13:00
views              | 38488304
icon               | https://avt.mkklcdnv6.com/43/w/1-1583465436.jpg
description        | From OSTNT: The Mythical Realm: A world of blood, a world where the strong triumph ov...

##### Chapter Download
```python
...

from manganelo import DownloadChapter

for chapter in manga_page.chapters:
	file = f"./Naruto {chapter.num}.pdf"

	dl = DownloadChapter(chapter.url, file)

	results = dl.results()

	if results.saved_ok:
		print(results.path)
```

##### Complete Usage
```python
search = SearchManga("Raid", threaded=False)

results = list(search.results())

best_result = results[0]

manga_info = MangaInfo(best_result.url, threaded=False)

manga_page = manga_info.results()

for chapter in manga_page.chapters:
	file = f"./Raid {chapter.num}.pdf"

	dl = DownloadChapter(chapter.url, file)

	results = dl.results()

	if results.saved_ok:
		print(results.path, results.percent_saved)
```

Contact Me
-
I am happy to respond to emails at **joshuanixonofficial@gmail.com**