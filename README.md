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

##### Manga Main Page (Home screen of each manga)

```python
info = MangaInfo("https://manganelo.com/manga/martial_gods_space")

print("Title:", info.title)
print("Authors:", info.authors)
print("Num. Chapters:", len(info.chapters))
print("Genres:", info.genres)
print("Status:", info.status)
```