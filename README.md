[![Downloads](https://pepy.tech/badge/manganelo)](https://pepy.tech/project/manganelo) [![Downloads](https://pepy.tech/badge/manganelo/month)](https://pepy.tech/project/manganelo/month) [![Downloads](https://pepy.tech/badge/manganelo/week)](https://pepy.tech/project/manganelo/week)

# Unofficial Manganelo (Manganato) API

Installation
-
**Python 3.7+ (latest version requires version Py3.9)**
```cmd
pip install manganelo
```

Change Log
-
`1.6.0` - **results** method is now a cached property

Examples
-

#### Legacy Examples (will be removed soon)
```python
search = SearchManga("Raid", threaded=False)

results = search.results

best_result = results[0]

manga_info = MangaInfo(best_result.url, threaded=False)

manga_page = manga_info.results

for chapter in manga_page.chapters:
	file = f"./Raid {chapter.num}.pdf"

	dl = DownloadChapter(chapter.url, file)

	results = dl.results

	if results.saved_ok:
		print(results.path, results.percent_saved)
```

#### Rewrite Version (will soon become standard)
```python
import manganelo.rewrite as manganelo

results = manganelo.search("Naruto")

for r in results:
    print(r.title, r.views)

    chapters = r.chapter_list()

    for c in chapters:
        print(f"#{c.chapter} | {c.title}")

        chapter_path = c.download(path=f"./Chapter {c.chapter}.pdf")

```
