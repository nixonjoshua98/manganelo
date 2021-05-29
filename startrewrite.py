
import manganelo.rewrite as manganelo

results = manganelo.search(title="Naruto")

page = manganelo.manga_page(url="http://manganelo.com/manga/black_clover")

path = page.download_icon(path="./Icon.png")

print(path)

chapters = results[0].chapter_list()

path = chapters[0].download(path=f"./Chapter.pdf")

print(path)
