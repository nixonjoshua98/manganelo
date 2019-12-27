# Unofficial Manganelo API

Package to scrape the website Manganelo (and Mangakakalot).

Need something? Send me an email at nixonjoshua98 (at) gmail (dot) com.

## Installation

**Python 3.7.x**
```cmd
pip install manganelo
```

## Usage

**Getting the chapter list of every search result**
```python
import manganelo

search_object = manganelo.SearchManga("Naruto")

search_object.start()

for result in search_object.results:
    chapters = manganelo.MangaChapters(result.url, start=True)
    
    for c in chapters.results:
        print(c.url, c.chapter_num)
```

## TODO
- Download chapters (completed but need to add error handling)