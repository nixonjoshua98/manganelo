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
`1.19.0`
- Removed legacy code and replaced default objects with the previous 'rewrite'
- Some methods have been renamed

`1.6.0` 
- **results** method is now a cached property

Examples
-

```python
import manganelo

results = manganelo.get_search_results("Naruto")

for r in results:
    print(r.title, r.views)

    chapters = r.chapter_list()
    
    icon_path = r.download_icon("./icon.png")

    for c in chapters:
        print(f"#{c.chapter} | {c.title}")

        chapter_path = c.download(f"./Chapter {c.chapter}.pdf")

```
