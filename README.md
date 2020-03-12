# Unofficial Manganelo API

Package to scrape the website Manganelo (and Mangakakalot).

_nixonjoshua98@gmail.com_

## Installation

**Python 3.7.x**
```cmd
pip install manganelo
```

## Example

```python
with MangaSearch("Naruto") as search_object:
    results = list(search_object.results())
    
    naruto = results[0]

with ChapterList(naruto.url) as chap_list:
    chapters = list(chap_list.results())

with MangaInfo(naruto.url) as info:
    naruto_info = info.result()

print("Title:", naruto_info.title)
print("Authors:", ",".join(naruto_info.authors))
print("Total Chapters:", len(chapters))
print("Latest Chapter URL:", chapters[-1].url)
```