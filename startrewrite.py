
import manganelo.rewrite as manganelo

results = manganelo.search(title="Naruto")

page = manganelo.manga_page(url="https://manganelo.com/manga/uit2233589789789")

path = page.download_icon(path="./Icon.png")

print(path)

chapters = results[0].chapter_list()

path = chapters[0].download(path=f"./Chapter.pdf")

print(path)
