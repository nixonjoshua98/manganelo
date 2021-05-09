[![Downloads](https://pepy.tech/badge/manganelo)](https://pepy.tech/project/manganelo) [![Downloads](https://pepy.tech/badge/manganelo/month)](https://pepy.tech/project/manganelo/month) [![Downloads](https://pepy.tech/badge/manganelo/week)](https://pepy.tech/project/manganelo/week)

# Unofficial Manganelo API

###### Package to scrape the Manganelo website. Want to contribute? Pull requests are encouraged!

Installation
-
**Python 3.7+**
```cmd
pip install manganelo
```

Change Log
-
`1.6.0` - **results** method is now a cached property

Examples
-

#### Standard Usage
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

#### Rewrite Version (will eventually become standard)
```python
import manganelo.rewrite as manganelo

results = manganelo.search(title="Naruto")

first = results[0]

chapters = first.chapter_list()
# manganelo.chapter_list(url=first.url)

chap_one = chapters[0]

path = chap_one.download(path=f"D:\\Repos\\manganelo\\{chap_one.title}.pdf")
# manganelo.download(url=chap_one.url, path=...)

print(path)  # D:\Repos\manganelo\Vol.1 Chapter 0  Naruto Pilot Manga.pdf
```

Contact Me
-
Email: joshuanixonofficial@gmail.com
