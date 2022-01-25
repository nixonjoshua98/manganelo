[![Downloads](https://pepy.tech/badge/manganelo)](https://pepy.tech/project/manganelo) [![Downloads](https://pepy.tech/badge/manganelo/month)](https://pepy.tech/project/manganelo/month) [![Downloads](https://pepy.tech/badge/manganelo/week)](https://pepy.tech/project/manganelo/week)

# Unofficial Manganelo (Manganato) API

Installation
-
**Python 3.7+ (latest version requires Python 3.9+)**
```cmd
pip install manganelo
```

Examples
-
```python
import manganelo

home_page = manganelo.get_home_page()

results = manganelo.get_search_results("Naruto")

for r in results:
    print(r.title, r.views)

    chapters = r.chapter_list()
    
    icon_path = r.download_icon("./icon.png")

    for c in chapters:
        print(f"#{c.chapter} | {c.title}")

        chapter_path = c.download(f"./Chapter {c.chapter}.pdf")
```