# Unofficial Manganelo API

#### Package to scrape the website Manganelo (and Mangakakalot).

nixonjoshua98 at gmail dot com

## Installation

**Python 3.7.x**
```cmd
pip install manganelo
```

## Example

```python
naruto = SearchManga("Naruto")[0]

info = MangaInfo(naruto.url)

for k, v in info.items():
    print(f"{k}: {v}")
```