# Unofficial Manganelo API

Package to scrape the website Manganelo (and Mangakakalot).

Need something? Send me an email at nixonjoshua98 (at) gmail (dot) com.

## Installation

**Python 3.7.x**
```cmd
pip install manganelo
```

## Usage

**Searching**
```python
import manganelo

search_object = manganelo.SearchManga("Naruto")

search_object.search()

for result in search_object.results:
    print(result.title)
```

## TODO
- Add chapter list extraction (completed but need to package it up)
- Download chapters (completed but need to add error handling)