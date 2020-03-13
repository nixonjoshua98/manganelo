# Unofficial Manganelo API

#### Package to scrape the website Manganelo (and Mangakakalot).

_nixonjoshua98 at gmail dot com_

## Installation

**Python 3.7.x**
```cmd
pip install manganelo
```

## Examples
##### Searching

```python
results = MangaSearch("God")

for r in results:
    print(r.title, r.url)
```

##### Information

```python
info = MangaInfo("https://manganelo.com/manga/martial_gods_space")

print("Title:", info.title)
print("Authors:", info.authors)
print("Genres:", info.genres)
print("Alt Titles:", info.alt_titles)
print("Status:", info.status)
```

##### Chapter List

```python
chapters = ChapterList("https://manganelo.com/manga/everlasting_god_of_sword")

for c in chapters:
    print(c.url, c.chapter_num)
```